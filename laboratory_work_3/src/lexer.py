from tokenner import Tokenner, TokenType

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.set_current_char()
        
    def __str__(self):
        """String representation of the class instance."""
        return f"Lexer({self.text})"
    
    def __repr__(self):
        """String representation of the class instance."""
        return self.__str__()
    
    def set_current_char(self):
        """Set the `current_char` variable."""
        if self.pos > len(self.text) - 1:
            return None
        else:
            return self.text[self.pos]

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        self.current_char = self.set_current_char()

    def skip_whitespace(self):
        """Skip whitespaces in the text."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            elif self.current_char.isdigit():
                return Tokenner(TokenType.INTEGER, self.integer())

            elif self.current_char == "+":
                self.advance()
                return Tokenner(TokenType.PLUS, "+")

            elif self.current_char == "-":
                self.advance()
                return Tokenner(TokenType.MINUS, "-")

            elif self.current_char == "*":
                self.advance()
                return Tokenner(TokenType.MUL, "*")

            elif self.current_char == "/":
                self.advance()
                return Tokenner(TokenType.DIV, "/")

            elif self.current_char == "(":
                self.advance()
                return Tokenner(TokenType.LPAREN, "(")

            elif self.current_char == ")":
                self.advance()
                return Tokenner(TokenType.RPAREN, ")")

            else:
                unknown = self.current_char
                self.advance()
                return Tokenner(TokenType.UNKNOWN, unknown)

        return Tokenner(TokenType.EOF, None)
    
    def tokenize(self):
        """Return a list of tokens from the text."""
        tokens = []
        while (token := self.get_next_token()).type != TokenType.EOF:
            tokens.append(token)
        tokens.append(token)
        return tokens
   