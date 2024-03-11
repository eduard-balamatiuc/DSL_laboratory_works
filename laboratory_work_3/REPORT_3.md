# Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Eduard Balamatiuc

----

## Theory
The term lexer comes from lexical analysis which, in turn, represents the process of extracting lexical tokens from a string of characters. There are several alternative names for the mechanism called lexer, for example tokenizer or scanner. The lexical analysis is one of the first stages used in a compiler/interpreter when dealing with programming, markup or other types of languages.

    The tokens are identified based on some rules of the language and the products that the lexer gives are called lexemes. So basically the lexer is a stream of lexemes. Now in case it is not clear what's the difference between lexemes and tokens, there is a big one. The lexeme is just the byproduct of splitting based on delimiters, for example spaces, but the tokens give names or categories to each lexeme. So the tokens don't retain necessarily the actual value of the lexeme, but rather the type of it and maybe some metadata.


## Objectives:
1. Understand what lexical analysis [1] is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

## Implementation description

- First step of my implementation was to create a class for the types of tokens that I will use in the lexer. I created a class called TokenType. The type is an enum, and the value is a string. The enum contains the types of tokens that I will use in the lexer. The types are: INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF and UNKNOWN.

```python
class TokenType(str, Enum):
    """The available token types."""
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"
```
After that, I created a classs named Token which will represent the token objects which the lexer will operate with. The class has two fields: type and value. The type is of type TokenType and the value is of type any. The value will be the actual value of the token, for example the number 5, the plus sign, the minus sign, etc.

```python
class Tokenner:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance."""
        return f"Token({self.type}, {self.value})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.type == other.type and self.value == other.value
```

The next step was to create the lexer class. The lexer class contains the following main methods:

- `__init__` - the constructor of the class. It takes a string as an argument and sets the text, pos and current_char fields.
```python
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.set_current_char()
```

- `__str__` & `__repr__`- returns a string representation of the class instance.
```python
    def __str__(self):
        """String representation of the class instance."""
        return f"Lexer({self.text})"

    def __repr__(self):
        """String representation of the class instance."""
        return self.__str__()
```

- `set_current_char` - sets the current_char variable. If the pos is greater than the length of the text, it sets the current_char to None, otherwise it sets it to the character at the position pos.
```python
def set_current_char(self):
        """Set the `current_char` variable."""
        if self.pos > len(self.text) - 1:
            return None
        else:
            return self.text[self.pos]
```

- `advance` - advances the pos pointer and sets the current_char variable.
```python
    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        self.current_char = self.set_current_char()
```

- `skip_whitespace` - skips whitespaces in the text till the current_char is not a whitespace character.
```python
    def skip_whitespace(self):
        """Skip whitespaces in the text."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
```

- `integer` - returns a (multidigit) integer consumed from the input.
```python
    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
```

- `get_next_token` - the main method of the lexer. It returns the next token from the input.
```python
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
```

- `tokenize` - returns a list of tokens which represent the processed input text.
```python
    def tokenize(self):
        """Return a list of tokens from the text."""
        tokens = []
        while (token := self.get_next_token()).type != TokenType.EOF:
            tokens.append(token)
        tokens.append(token)
        return tokens
```

## Conclusions / Screenshots / Results
To conclude the laboratory work, I have implemented a simple lexer which can tokenize a simple arithmetic expression for integers. The lexer can tokenize the following types of tokens: INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF and UNKNOWN. I did that by creating a class for the types of tokens, a class for the token objects and a class for the lexer. The lexer class contains the main methods for the lexer. The lexer can tokenize a simple arithmetic expression and return a list of tokens which represent the processed input text.

## References
1. [Lexical Analysis](https://en.wikipedia.org/wiki/Lexical_analysis)
2. [Python Docs](https://www.python.org/doc/)