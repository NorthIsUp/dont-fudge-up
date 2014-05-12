from dfu.flake8.lib import BaseASTCheck, BaseChecker


class DFUChecker(BaseChecker):
    name = 'dfu'
    version = '1.0.0'


class DangerousImportCheck(BaseASTCheck):
    """
    Checks for potentially dangerous imports
    """

    D421 = 'Forbidden import for production'
    D422 = 'Cautioned import for production'

    watched_imports = {
        'debug': 'D421',
        'pdb': 'D422',
    }

    def visit_import(self, node, parents):
        watched_imports = self.watched_imports
        names = [_.name for _ in node.names if _.name in watched_imports]

        for name in names:
            yield self.err(node, watched_imports[name])


class PrintCheck(BaseASTCheck):
    """
    Checks for potentially dangerous imports
    """

    D423 = 'WHY U LEAVE A PRINT?'

    def visit_print(self, node, parents):
        yield self.err(node, 'D423')


class DebuggerCheck(BaseASTCheck):

    D424 = 'pdb.set_trace is fatal in production'
    D425 = 'set_trace may be fatal in production (set_trace may be be from pdb)'

    def visit_call(self, node, parrents):
        func_name = getattr(node.func, 'attr', None) or getattr(node.func, 'id', None)
        func_module = getattr(node.func, 'value', None)

        if func_name == 'set_trace':
            if func_module and func_module.id in ('pdb', 'ipdb', 'bpdb'):
                yield self.err(node, 'D424')
            else:
                yield self.err(node, 'D424')
