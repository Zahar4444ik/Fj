from regex.lexer import TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def consume(self, expected_token_type):
        """
        Check method - checks whether the current token is of the expected type.
        If so, it moves on to the next token. If not, it throws an error.

        This method implements predictive analysis - we expect a specific token
        based on grammatical rules.
        """
        if self.current_token.type == expected_token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Syntax error: expected token {expected_token_type}, "
                              f"acquired {self.current_token.type}")

    def parse_regular(self):
        """
        regular ::= alternative
        """

        alternative = self.parse_alternative()
        return {"type": "regular", "children": [alternative]}

    def parse_alternative(self):
        """
        alternative ::= sequence {'|' sequence} ліва
        alternative ::= sequence ['|' alternative] права
        """
        seq = self.parse_sequence()
        children = [seq]

        while self.current_token.type == TokenType.PIPE:
            self.consume(TokenType.PIPE)
            children.append({"type": "symbol", "value": "<PIPE>"})
            seq = self.parse_sequence()
            children.append(seq)

        return {"type": "alternative", "children": children}

    def parse_sequence(self):
        """
        sequence ::= element {element}
        """
        elements = [self.parse_element()]

        while self.current_token.type in (TokenType.SYMBOL, TokenType.LPAREN, TokenType.LBRACE, TokenType.LBRACKET):
            elements.append(self.parse_element())

        return {"type": "sequence", "children": elements}

    def parse_element(self):
        """
        element ::= symbol | '(' regular ')' | '{' regular '}' | '[' regular ']'
        """
        if self.current_token.type == TokenType.SYMBOL:
            symbol = self.parse_symbol()
            return {"type": "element", "children": [symbol]}
        elif self.current_token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            lparen = {"type": "symbol", "value": "<LPAREN>"}
            regular = self.parse_regular()
            self.consume(TokenType.RPAREN)
            rparen = {"type": "symbol", "value": "<RPAREN>"}
            return {"type": "element", "children": [lparen, regular, rparen]}
        elif self.current_token.type == TokenType.LBRACE:
            self.consume(TokenType.LBRACE)
            lbrace = {"type": "symbol", "value": "<LBRACE>"}
            regular = self.parse_regular()
            self.consume(TokenType.RBRACE)
            rbrace = {"type": "symbol", "value": "<RBRACE>"}
            return {"type": "element", "children": [lbrace, regular, rbrace]}
        elif self.current_token.type == TokenType.LBRACKET:
            self.consume(TokenType.LBRACKET)
            lbracket = {"type": "symbol", "value": "<LBRACKET>"}
            regular = self.parse_regular()
            self.consume(TokenType.RBRACKET)
            rbracket = {"type": "symbol", "value": "<RBRACKET>"}
            return {"type": "element", "children": [lbracket, regular, rbracket]}
        else:
            raise SyntaxError(
                f"Syntax error: expected SYMBOL, LPAREN, LBRACE, or LBRACKET, got {self.current_token.type} - {self.current_token.attribute}"
            )

    def parse_symbol(self):
        if self.current_token.type == TokenType.SYMBOL:
            value = self.current_token.attribute
            self.consume(TokenType.SYMBOL)
            return {"type": "symbol", "value": value}
        else:
            raise SyntaxError(
                f"Syntax error: expected SYMBOL, got {self.current_token.type}"
            )

    def parse(self):
        tree = self.parse_regular()
        if self.current_token.type != TokenType.EOF:
            raise SyntaxError(
                f"Syntax error: unexpected token {self.current_token.type} at end of input"
            )
        return tree
