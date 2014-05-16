from dfu.flake8.lib import BaseASTCheck, BaseChecker
from dfu import VERSION
from dfu import messages


class DFUChecker(BaseChecker):
    name = 'dont-fudge-up'
    version = VERSION

#: create a base class that has all of the error codes in it
DFUASTCheck = type('DFUASTCheck', (BaseASTCheck, ), messages.get_flake8_messages())


class DangerousImportCheck(DFUASTCheck):
    """
    Checks for potentially dangerous imports
    """

    watched_imports = {
        'debug': messages.forbidden_import,
        'pdb': messages.cautioned_import,
    }

    def visit_import(self, node, parents):
        watched_imports = self.watched_imports
        names = [_.name for _ in node.names if _.name in watched_imports]

        for name in names:
            yield self.err(node, watched_imports[name])


class PrintCheck(DFUASTCheck):
    """
    Checks for potentially dangerous imports
    """

    def visit_print(self, node, parents):
        yield self.err(node, 'D001')


class DebuggerCheck(DFUASTCheck):

    def visit_call(self, node, parrents):
        func_name = getattr(node.func, 'attr', None) or getattr(node.func, 'id', None)
        func_module = getattr(node.func, 'value', None)

        if func_name == 'set_trace':
            if func_module and func_module.id in ('pdb', 'ipdb', 'bpdb'):
                yield self.err(node, messages.forbidden_set_trace)
            else:
                yield self.err(node, messages.cautioned_set_trace)
