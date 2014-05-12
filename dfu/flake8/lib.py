# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
from collections import deque

try:
    import ast
    from ast import iter_child_nodes
except ImportError:
    from flake8.util import ast, iter_child_nodes

if sys.version_info[0] < 3:
    def _unpack_args(args):
        ret = []
        for arg in args:
            if isinstance(arg, ast.Tuple):
                ret.extend(_unpack_args(arg.elts))
            else:
                ret.append(arg.id)
        return ret

    def get_arg_names(node):
        return _unpack_args(node.args.args)
else:
    def get_arg_names(node):
        pos_args = [arg.arg for arg in node.args.args]
        kw_only = [arg.arg for arg in node.args.kwonlyargs]
        return pos_args + kw_only


class _ASTCheckMeta(type):
    def __init__(self, class_name, bases, namespace):
        try:
            self._checks.append(self())
        except AttributeError:
            self._checks = []


def _err(self, node, code):
    lineno, col_offset = node.lineno, node.col_offset
    if isinstance(node, ast.ClassDef):
        lineno += len(node.decorator_list)
        col_offset += 6
    elif isinstance(node, ast.FunctionDef):
        lineno += len(node.decorator_list)
        col_offset += 4
    return (lineno, col_offset, '%s %s' % (code, getattr(self, code)), self)
BaseASTCheck = _ASTCheckMeta('BaseASTCheck', (object,),
                             {'__doc__': "Base for AST Checks.", 'err': _err})


class BaseChecker(object):
    """Checker of PEP-8 Naming Conventions."""
    name = NotImplemented
    version = NotImplemented

    def __init__(self, tree, filename):
        self.visitors = BaseASTCheck._checks
        self.parents = deque()
        self._node = tree

    def run(self):
        return self.visit_tree(self._node) if self._node else ()

    def visit_tree(self, node):
        for error in self.visit_node(node):
            yield error
        self.parents.append(node)
        for child in iter_child_nodes(node):
            for error in self.visit_tree(child):
                yield error
        self.parents.pop()

    def visit_node(self, node):
        if isinstance(node, ast.ClassDef):
            self.tag_class_functions(node)
        elif isinstance(node, ast.FunctionDef):
            self.find_global_defs(node)

        method = 'visit_' + node.__class__.__name__.lower()
        for visitor in self.visitors:
            if not hasattr(visitor, method):
                continue
            for error in getattr(visitor, method)(node, self.parents):
                yield error

    def tag_class_functions(self, cls_node):
        """Tag functions if they are methods, classmethods, staticmethods"""
        # tries to find all 'old style decorators' like
        # m = staticmethod(m)
        late_decoration = {}
        for node in iter_child_nodes(cls_node):
            if not (isinstance(node, ast.Assign) and
                    isinstance(node.value, ast.Call) and
                    isinstance(node.value.func, ast.Name)):
                continue
            func_name = node.value.func.id
            if func_name in ('classmethod', 'staticmethod'):
                meth = (len(node.value.args) == 1 and node.value.args[0])
                if isinstance(meth, ast.Name):
                    late_decoration[meth.id] = func_name

        # iterate over all functions and tag them
        for node in iter_child_nodes(cls_node):
            if not isinstance(node, ast.FunctionDef):
                continue

            node.function_type = 'method'
            if node.name == '__new__':
                node.function_type = 'classmethod'

            if node.name in late_decoration:
                node.function_type = late_decoration[node.name]
            elif node.decorator_list:
                names = [d.id for d in node.decorator_list
                         if isinstance(d, ast.Name) and
                         d.id in ('classmethod', 'staticmethod')]
                if names:
                    node.function_type = names[0]

    def find_global_defs(self, func_def_node):
        global_names = set()
        nodes_to_check = deque(iter_child_nodes(func_def_node))
        while nodes_to_check:
            node = nodes_to_check.pop()
            if isinstance(node, ast.Global):
                global_names.update(node.names)

            if not isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                nodes_to_check.extend(iter_child_nodes(node))
        func_def_node.global_names = global_names
