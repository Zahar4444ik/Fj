from enum import Enum, auto


class TokenType(Enum):
    SYMBOL = auto()  # Symbol
    PIPE = auto()  # Operátor '|' (alternácia)
    LPAREN = auto()  # Ľavá zátvorka '('
    RPAREN = auto()  # Pravá zátvorka ')'
    LBRACE = auto()  # Ľavá zložená zátvorka '{'
    RBRACE = auto()  # Pravá zložená zátvorka '}'
    LBRACKET = auto()  # Ľavý hranatý zátvor '['
    RBRACKET = auto()  # Pravý hranatý zátvor ']'
    EOF = auto()  # Koniec vstupu (End Of File)


class Token:
    def __init__(self, type, value=None):
        self.type = type  # Typ tokenu (z enum TokenType)
        self.attribute = value  # Hodnota tokenu

    def __repr__(self):
        # Reťazcová reprezentácia tokenu
        if self.attribute is not None:
            return f"Token({self.type}, {self.attribute})"
        return f"Token({self.type})"


# Lexikálny analyzátor - rozpoznáva a extrahuje tokeny zo vstupného reťazca
class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.pos = 0
        self.current_char = self.input_text[0] if input_text else None

    def advance(self):
        """Posunie pozíciu na ďalší znak a aktualizuje current_char.
        Ak sa dostane za koniec textu, nastaví current_char na None."""
        self.pos += 1
        if self.pos < len(self.input_text):
            self.current_char = self.input_text[self.pos]
        else:
            self.current_char = None  # Dosiahli sme koniec textu

    def skip_whitespace(self):
        """Preskočí všetky medzery a nové riadky vo vstupe."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def symbol(self):
        """Vracia token typu SYMBOL."""
        if self.current_char.isalpha() or self.current_char.isdigit():
            char = self.current_char
            self.advance()
            return Token(TokenType.SYMBOL, f"<SYMBOL,{char}>")
        raise ValueError(f"Nerozpoznaný symbol: '{self.current_char}' v pozicií {self.pos}")

    def get_next_token(self):
        """Hlavná metóda lexikálneho analyzátora.
        Analyzuje text a vracia ďalší token v poradí."""
        while self.current_char is not None:
            # Ignorovanie medzier a formátovanie
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Rozpoznávanie symbolov
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

            raise ValueError(f"Nerozpoznaný znak: '{self.current_char}'")

        return Token(TokenType.EOF)
