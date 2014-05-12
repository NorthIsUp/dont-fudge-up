from dfu.flake8.lib import BaseASTCheck, BaseChecker
from dfu import VERSION


class DFUChecker(BaseChecker):
    name = 'dont-fudge-up'
    version = VERSION


class DFUASTCheck(BaseASTCheck):
    #: D0xx is stylistically bad for production
    D001 = 'WHY U LEAVE A PRINT?'

    #: D1xx are cautioned items for production
    D101 = 'Cautioned import for production'
    D102 = 'set_trace may be fatal in production (set_trace might be from pdb)'

    #: D5xx are forbidden items for production
    D501 = 'Forbidden import for production'
    D502 = 'pdb.set_trace is forbidden in production'


class DangerousImportCheck(DFUASTCheck):
    """
    Checks for potentially dangerous imports
    """

    cautioned_import = 'D101'
    forbidden_import = 'D501'

    watched_imports = {
        'debug': forbidden_import,
        'pdb': cautioned_import,
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

    cautioned_set_trace = 'D102'
    forbidden_set_trace = 'D502'

    def visit_call(self, node, parrents):
        func_name = getattr(node.func, 'attr', None) or getattr(node.func, 'id', None)
        func_module = getattr(node.func, 'value', None)

        if func_name == 'set_trace':
            if func_module and func_module.id in ('pdb', 'ipdb', 'bpdb'):
                yield self.err(node, self.forbidden_set_trace)
            else:
                yield self.err(node, self.cautioned_set_trace)
