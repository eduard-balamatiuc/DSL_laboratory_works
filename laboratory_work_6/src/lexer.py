import re
from tokenner import Tokenner, TokenType

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []
        self.tokenize()

    def __str__(self):
        """String representation of the class instance."""
        return f"Lexer({self.text})"

    def __repr__(self):
        """String representation of the class instance."""
        return self.__str__()

    def tokenize(self):
        """Tokenize the entire input text using regular expressions."""
        token_specification = [
            ('INTEGER',   r'\d+'),            # Integer
            ('PLUS',      r'\+'),             # Plus sign
            ('MINUS',     r'-'),              # Minus sign
            ('MUL',       r'\*'),             # Multiplication sign
            ('DIV',       r'\/'),             # Division sign
            ('LPAREN',    r'\('),             # Left Parenthesis
            ('RPAREN',    r'\)'),             # Right Parenthesis
            ('WHITESPACE', r'\s+'),           # Whitespace
            ('UNKNOWN',   r'.'),              # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        for mo in re.finditer(tok_regex, self.text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'WHITESPACE':
                continue
            elif kind == 'INTEGER':
                value = int(value)
            elif kind == 'UNKNOWN':
                raise Exception(f'Unexpected character: {value}')
            self.tokens.append(Tokenner(TokenType[kind], value))
        self.tokens.append(Tokenner(TokenType.EOF, None))

    def get_next_token(self):
        """Return the next token from the token list."""
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        else:
            return Tokenner(TokenType.EOF, None)

# Example usage
lexer = Lexer("3 + 4 * (2 - 1) / 2")
print(lexer.tokens)