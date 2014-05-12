from pylint.checkers import BaseChecker

try:
    from pylint.interfaces import IAstroidChecker
except ImportError:
    # fallback to older pylint naming
    from pylint.interfaces import IASTNGChecker as IAstroidChecker


class DFUChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = 'missing_gettext'
    msgs = {
        'W4201': ('print at %s:%d', 'print', 'you left a print in your code'),
        'W4202': ('pdb imported %s:%d', 'import-pdb', 'pdb imported, probably not needed for production'),
        'F4203': ('import debug at %s:%d', 'import-debug', 'import debug will be fatal in production'),
        'F4204': ('pdb.set_trace at %s:%d', 'pdb-set_trace', 'pdb.set_trace will be fatal in production'),
    }

    # this is important so that your checker is executed before others
    priority = -1

    def visit_print(self, node):
        self.add_message('W4201', node=node, args=(node.frame().file, node.fromlineno))

    def visit_callfunc(self, node):
        if node.as_string() == 'pdb.set_trace()':
            self.add_message('F4204', node=node, args=(node.frame().file, node.fromlineno))

    def visit_import(self, node):
        if node.as_string() == 'import pdb':
            self.add_message('W4202', node=node, args=(node.frame().file, node.fromlineno))
        elif node.as_string() == 'import debug':
            self.add_message('F4203', node=node, args=(node.frame().file, node.fromlineno))


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(DFUChecker(linter))
