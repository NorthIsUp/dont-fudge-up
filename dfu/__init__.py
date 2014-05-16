try:
    VERSION = __import__('pkg_resources').get_distribution('dont-fudge-up').version
except Exception:  # pragma: no cover
    VERSION = 'unknown'


try:
    from pylint.utils import MSG_TYPES
except ImportError:
    MSG_TYPES = None


class Msg(str):

    """
    Container for lint messages.

    Messages can be converted to either a PyLint of Flake8 format.
    """

    def __new__(
        cls,
        id,
        msg='',
        symbol='',
        description='',
        options=(),
        pylint_type=''
    ):
        obj = super(Msg, cls).__new__(cls, symbol)
        obj.id = id
        obj.msg = msg or description
        obj.fmt = ''
        obj.description = description
        obj.options = options
        obj.symbol = symbol
        obj.pylint_type = pylint_type

        if pylint_type and MSG_TYPES and pylint_type not in MSG_TYPES:
            raise ValueError('pylint_type must be in pylint.utlis.MSG_TYPES')

        return obj

    def __str__(self):
        if self.fmt == 'pylint':
            letter, fill = self.pylint_type, '4'
        elif self.fmt == 'flake8':
            letter, fill = 'D', ''
        else:
            letter, fill = ''

        return '{letter}{fill}{msg:>03}'.format(letter=letter, fill=fill, msg=self.id)

    __eq__ = lambda self, value: value in (str(self), self.symbol, self.id)
    __getattr__ = lambda self, name: getattr(str(self), name)
    __getitem__ = lambda self, i: str(self)[i]
    __getslice__ = lambda self, i, j: str(self)[i:j]
    __hash__ = lambda self: hash(str(self))
    __len__ = lambda self: len(str(self))
    __repr__ = lambda self: '<{s.fmt} {cls} {s!s}: {s.symbol}>'.format(cls=self.__class__.__name__, s=self)
    upper = lambda self: self

    def pylint_message(self):
        self.fmt = 'pylint'
        return (self.msg, self.symbol, self.description) + ((self.options, ) if self.options else ())

    def flake8_message(self):
        self.fmt = 'flake8'
        return self.description
