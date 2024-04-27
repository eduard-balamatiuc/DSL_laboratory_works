import unittest
from lexer import Lexer
from tokenner import Tokenner, TokenType


class TestLexer(unittest.TestCase):
    def test_lexer_integer(self):
        """Test of integer token recognition."""
        lexer = Lexer("123")
        token = lexer.get_next_token()
        self.assertEqual(token, Tokenner(TokenType.INTEGER, 123))

    def test_lexer_plus(self):
        """Test of plus token recognition."""
        lexer = Lexer("+")
        token = lexer.get_next_token()
        self.assertEqual(token, Tokenner(TokenType.PLUS, "+"))

    def test_lexer_minus(self):
        """Test of minus token recognition."""
        lexer = Lexer("-")
        token = lexer.get_next_token()
        self.assertEqual(token, Tokenner(TokenType.MINUS, "-"))

    def test_lexer_mul(self):
        """Test of multiplication token recognition."""
        lexer = Lexer("*")
        token = lexer.get_next_token()
        self.assertEqual(token, Tokenner(TokenType.MUL, "*"))

    def test_lexer_div(self):
        """Test of division token recognition."""
        lexer = Lexer("/")
        token = lexer.get_next_token()
        self.assertEqual(token, Tokenner(TokenType.DIV, "/"))

    def test_lexer_lparen(self):
        """Test of left parenthesis token recognition."""
        lexer = Lexer("(")
        token = lexer.get_next_token()
        self.assertEqual(token, Tokenner(TokenType.LPAREN, "("))

    def test_lexer_rparen(self):
        """Test of right parenthesis token recognition."""
        lexer = Lexer(")")
        token = lexer.get_next_token()
        self.assertEqual(token, Tokenner(TokenType.RPAREN, ")"))

    def test_lexer_eof(self):
        """Test of end of file token recognition."""
        lexer = Lexer("")
        token = lexer.get_next_token()
        self.assertEqual(token, Tokenner(TokenType.EOF, None))

    def test_lexer_tokenize(self):
        """Test of the tokenize method."""
        lexer = Lexer("2 + 3")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Tokenner(TokenType.INTEGER, 2),
            Tokenner(TokenType.PLUS, "+"),
            Tokenner(TokenType.INTEGER, 3),
            Tokenner(TokenType.EOF, None)
        ])

    def test_lexer_tokenize_with_whitespace(self):
        """Test of the tokenize method with whitespace."""
        lexer = Lexer(" 2 + 3 ")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Tokenner(TokenType.INTEGER, 2),
            Tokenner(TokenType.PLUS, "+"),
            Tokenner(TokenType.INTEGER, 3),
            Tokenner(TokenType.EOF, None)
        ])

    def test_lexer_tokenize_with_parenthesis(self):
        """Test of the tokenize method with parenthesis."""
        lexer = Lexer("(2 + 3)")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Tokenner(TokenType.LPAREN, "("),
            Tokenner(TokenType.INTEGER, 2),
            Tokenner(TokenType.PLUS, "+"),
            Tokenner(TokenType.INTEGER, 3),
            Tokenner(TokenType.RPAREN, ")"),
            Tokenner(TokenType.EOF, None)
        ])

    def test_lexer_tokenize_with_mul_and_div(self):
        """Test of the tokenize method with multiplication and division."""
        lexer = Lexer("2 * 3 / 4")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Tokenner(TokenType.INTEGER, 2),
            Tokenner(TokenType.MUL, "*"),
            Tokenner(TokenType.INTEGER, 3),
            Tokenner(TokenType.DIV, "/"),
            Tokenner(TokenType.INTEGER, 4),
            Tokenner(TokenType.EOF, None)
        ])

    def test_lexer_tokenize_with_mul_and_div_and_parenthesis(self):
        """Test of the tokenize method with multiplication, division and parenthesis."""
        lexer = Lexer("2 * (3 / 4)")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Tokenner(TokenType.INTEGER, 2),
            Tokenner(TokenType.MUL, "*"),
            Tokenner(TokenType.LPAREN, "("),
            Tokenner(TokenType.INTEGER, 3),
            Tokenner(TokenType.DIV, "/"),
            Tokenner(TokenType.INTEGER, 4),
            Tokenner(TokenType.RPAREN, ")"),
            Tokenner(TokenType.EOF, None)
        ])

    def test_lexer_tokenize_with_mul_and_div_and_parenthesis_and_whitespace(self):
        """Test of the tokenize method with multiplication, division, parenthesis and whitespace."""
        lexer = Lexer(" 2 * ( 3 / 4 ) ")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Tokenner(TokenType.INTEGER, 2),
            Tokenner(TokenType.MUL, "*"),
            Tokenner(TokenType.LPAREN, "("),
            Tokenner(TokenType.INTEGER, 3),
            Tokenner(TokenType.DIV, "/"),
            Tokenner(TokenType.INTEGER, 4),
            Tokenner(TokenType.RPAREN, ")"),
            Tokenner(TokenType.EOF, None)
        ])

    def test_lexer_tokenize_with_float(self):
        """Test of the tokenize method with a float number."""
        lexer = Lexer("3.14")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Tokenner(TokenType.INTEGER, 3),
            Tokenner(TokenType.UNKNOWN, "."),
            Tokenner(TokenType.INTEGER, 14),
            Tokenner(TokenType.EOF, None)
        ])

    def test_multiple_unkown_characters(self):
        """Test of the tokenize method with multiple unknown characters."""
        lexer = Lexer("jafadskl ..dfsa")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Tokenner(TokenType.UNKNOWN, "j"),
            Tokenner(TokenType.UNKNOWN, "a"),
            Tokenner(TokenType.UNKNOWN, "f"),
            Tokenner(TokenType.UNKNOWN, "a"),
            Tokenner(TokenType.UNKNOWN, "d"),
            Tokenner(TokenType.UNKNOWN, "s"),
            Tokenner(TokenType.UNKNOWN, "k"),
            Tokenner(TokenType.UNKNOWN, "l"),
            Tokenner(TokenType.UNKNOWN, "."),
            Tokenner(TokenType.UNKNOWN, "."),
            Tokenner(TokenType.UNKNOWN, "d"),
            Tokenner(TokenType.UNKNOWN, "f"),
            Tokenner(TokenType.UNKNOWN, "s"),
            Tokenner(TokenType.UNKNOWN, "a"),
            Tokenner(TokenType.EOF, None)
        ])

if __name__ == "__main__":
    unittest.main()