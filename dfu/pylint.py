from __future__ import absolute_import

from pylint.checkers import BaseChecker

from dfu import messages

try:
    from pylint.interfaces import IAstroidChecker
except ImportError:
    # fallback to older pylint naming
    from pylint.interfaces import IASTNGChecker as IAstroidChecker


class BaseDfuChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'dont-fudge-up'

    # this is important so that your checker is executed before others
    priority = -1


class DfuPrintChecker(BaseDfuChecker):
    msgs = messages.get_pylint_messages(start='W40')
    print msgs

    def visit_print(self, node):
        self.add_message('warn-print', node=node)


class DfuWarningChecker(BaseDfuChecker):
    msgs = messages.get_pylint_messages(start='W41')

    def visit_import(self, node):
        if node.as_string() == 'import pdb':
            self.add_message(messages.cautioned_import, node=node)


class DfuFatalChecker(BaseDfuChecker):
    msgs = messages.get_pylint_messages(start='F45')

    def visit_callfunc(self, node):
        if node.as_string() == 'pdb.set_trace()':
            self.add_message(messages.forbidden_set_trace, node=node)

    def visit_import(self, node):
        if node.as_string() == 'import debug':
            self.add_message(messages.forbidden_import, node=node)


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(DfuPrintChecker(linter))
    linter.register_checker(DfuFatalChecker(linter))
    linter.register_checker(DfuWarningChecker(linter))
