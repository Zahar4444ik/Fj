from enum import Enum, auto


class TokenType(Enum):
    SYMBOL = auto()  # Symbol
    PIPE = auto()  # '|'
    LPAREN = auto()  # '('
    RPAREN = auto()  # ')'
    LBRACE = auto()  # '{'
    RBRACE = auto()  # '}'
    LBRACKET = auto()  # '['
    RBRACKET = auto()  # ']'
    EOF = auto()  # (End Of File)


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.attribute = value

    def __repr__(self):
        if self.attribute is not None:
            return f"Token({self.type}, {self.attribute})"
        return f"Token({self.type})"


class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.pos = 0
        self.current_char = self.input_text[0] if input_text else None

    def advance(self):
        """Moves the position to the next character and updates current_char.
            If it reaches the end of the text, it sets current_char to None."""
        self.pos += 1
        if self.pos < len(self.input_text):
            self.current_char = self.input_text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        """Skips all spaces and new lines in the input."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def symbol(self):
        """Returns a token of type SYMBOL."""
        if self.current_char.isalpha() or self.current_char.isdigit():
            char = self.current_char
            self.advance()
            return Token(TokenType.SYMBOL, char)
        raise ValueError(f"Unrecognized symbol: '{self.current_char}' in position {self.pos}")

    def get_next_token(self):
        """The main method of the lexical analyzer.
        It analyzes the text and returns the next token in order."""
        while self.current_char is not None:
            # Ignoring spaces and formatting
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Symbol recognition
            if self.current_char.isalpha() or self.current_char.isdigit():
                return self.symbol()

            if self.current_char == '|':
                self.advance()
                return Token(TokenType.PIPE)

            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE)

            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE)

            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET)

            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET)

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN)

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN)

            raise ValueError(f"Unrecognized character: '{self.current_char}'")

        return Token(TokenType.EOF)
