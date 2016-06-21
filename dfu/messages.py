from dfu import Msg

#: 0xx is stylistically bad for production
cautioned_print = Msg(
    id=1,
    symbol='warn-print',
    description='WHY U LEAVE A PRINT?',
    pylint_type='W'
)

#: 1xx are cautioned items for production
cautioned_import = Msg(
    id=101,
    symbol='warn-import',
    description='Cautioned import for production',
    pylint_type='W'
)

cautioned_set_trace = Msg(
    id=102,
    symbol='warn-set-trace',
    description='set_trace may be fatal in production (set_trace might be from pdb)',
    pylint_type='W'
)

#: 5xx are forbidden items for production
forbidden_import = Msg(
    id=501,
    symbol='fatal-import',
    description='Forbidden import for production',
    pylint_type='F'
)

forbidden_set_trace = Msg(
    id=502,
    symbol='fatal-set-trace',
    description='pdb.set_trace is forbidden in production',
    pylint_type='F'
)


def _get_messages_dict(func, start=''):
    all_messages = dict((msg, getattr(msg, func)()) for msg in globals().values() if isinstance(msg, Msg))
    return dict((k, v) for k, v in all_messages.items() if str(k).startswith(start))


def get_flake8_messages(start=''):
    """
    Get the dict of flake8 messages that start with :param start:
    """
    return _get_messages_dict('flake8_message', start=start)


def get_pylint_messages(start=''):
    """
    Get the dict of pylint messages that start with :param start:
    """
    return _get_messages_dict('pylint_message', start=start)
