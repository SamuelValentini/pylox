from pylox.scanner import Scanner
from pylox.token import TokenType
import unittest
from unittest.mock import patch


class TestScanner(unittest.TestCase):

    def test_singleCharacter(self):
        expected = [TokenType.PLUS, TokenType.MINUS,
                    TokenType.COMMA, TokenType.SEMICOLON,
                    TokenType.STAR, TokenType.EOF]

        scanner = Scanner("+ - , ; *")
        tokens = scanner.scanTokens()
        for token, expected in zip(tokens, expected):
            self.assertEqual(token.type, expected)


    def test_doubleCharacter(self):
        expected = [TokenType.EQUAL, TokenType.EQUAL_EQUAL,
                    TokenType.MINUS, TokenType.LESS_EQUAL,
                    TokenType.EQUAL, TokenType.GREATER, TokenType.EOF]

        scanner = Scanner("= == - <= =>")
        tokens = scanner.scanTokens()
        for token, expected in zip(tokens, expected):
            self.assertEqual(token.type, expected)


    def test_error(self):

        with patch("pylox.lox.error") as mock_error:
            scanner = Scanner("@")
            tokens = scanner.scanTokens()
            mock_error.assert_called_once_with(1, "@ Unexpected character.")

        with patch("pylox.lox.error") as mock_error:
            scanner = Scanner("+\n@")
            tokens = scanner.scanTokens()
            mock_error.assert_called_once_with(2, "@ Unexpected character.")

    def test_slash(self):
        expected = [TokenType.SLASH, TokenType.MINUS, TokenType.EOF]
        scanner = Scanner("/ -")
        tokens = scanner.scanTokens()
        for token, expected in zip(tokens, expected):
            self.assertEqual(token.type, expected)


    def test_comment(self):
        with patch("pylox.lox.error") as mock_error:
            scanner = Scanner("//@ this is a comment")
            tokens = scanner.scanTokens()
            mock_error.assert_not_called

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)

    def test_multiLineComment(self):
        with patch("pylox.lox.error") as mock_error:
            scanner = Scanner("//@ this is a comment\n+")
            tokens = scanner.scanTokens()
            mock_error.assert_not_called

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.PLUS)
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_string(self):
        scanner = Scanner('"Hello"')
        tokens = scanner.scanTokens()
        self.assertEqual(tokens[0].literal, "Hello")
        self.assertEqual(tokens[0].lexeme, '"Hello"')

        with patch("pylox.lox.error") as mock_error:
            scanner = Scanner('"Unterminated string')
            tokens = scanner.scanTokens()
            mock_error.assert_called_once_with(1, "Unterminated string")

    def test_number(self):
        scanner = Scanner("12.34+1")
        tokens = scanner.scanTokens()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertAlmostEqual(tokens[0].literal, 12.34)
        self.assertEqual(tokens[0].lexeme, "12.34")

        self.assertEqual(tokens[1].type, TokenType.PLUS)
        self.assertEqual(tokens[1].lexeme, "+")

        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertAlmostEqual(tokens[2].literal, 1)
        self.assertEqual(tokens[2].lexeme, "1")



if __name__ == '__main__':
    unittest.main()
