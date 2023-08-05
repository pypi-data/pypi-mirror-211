# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring

class Token:

    """
    Token is the class that encapsulates a part of a source code: number, string or something else
    """

    Nil: str = 'Nil'
    Slice: str = 'Slice'
    Number: str = 'Number'
    String: str = 'String'
    Keyword: str = 'Keyword'
    Boolean: str = 'Boolean'
    Identifier: str = 'Identifier'
    OpeningParen: str = 'OpeningParen'
    ClosingParen: str = 'ClosingParen'
    InlineFunMarker: str = 'InlineFunMarker'
    CommentedMarker: str = 'CommentedMarker'

    _type: str
    _value: str
    _position: tuple

    def __init__(self, _type: str, _value: str, _pos: tuple) -> None:

        """Initializes Token instance"""

        self._type = _type
        self._value = _value
        self._position = _pos  # <---- filename and line/char numbers

    def type(self) -> str:

        """Return token type"""

        return self._type

    def value(self) -> str:

        """Return token value"""

        return self._value

    def position(self) -> tuple:

        """Return token position"""

        return self._position

    def is_nil(self) -> bool:

        """Just a handy shortcut"""

        return self._type == Token.Nil

    def is_slice(self) -> bool:

        """Just a handy shortcut"""

        return self._type == Token.Slice

    def is_number(self) -> bool:

        """Just a handy shortcut"""

        return self._type == Token.Number

    def is_string(self) -> bool:

        """Just a handy shortcut"""

        return self._type == Token.String

    def is_boolean(self) -> bool:

        """Just a handy shortcut"""

        return self._type == Token.Boolean

    def is_identifier(self) -> bool:

        """Just a handy shortcut"""

        return self._type == Token.Identifier

    def __str__(self) -> str:

        """Override __str__ method"""

        return f'Token<{self._type}>: {self._value}'

    def __repr__(self) -> str:

        """Override __repr__ method"""

        return self.__str__()  # in order to simplify debugging, make Token printing a bit fancier
