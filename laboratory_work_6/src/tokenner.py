from enum import Enum


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