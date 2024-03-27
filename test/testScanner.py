from pylox.scanner import Scanner
from pylox.token import TokenType
from pylox.errorHandler import ErrorHandler
import unittest
from unittest.mock import MagicMock, patch


class TestScanner(unittest.TestCase):
    def setUp(self):
        self.errorHandler = ErrorHandler()
        self.errorHandler.error = MagicMock()

    def test_singleCharacter(self):
        expected = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.COMMA,
            TokenType.SEMICOLON,
            TokenType.STAR,
            TokenType.EOF,
        ]

        scanner = Scanner("+ - , ; *", self.errorHandler)
        tokens = scanner.scanTokens()
        for token, expected in zip(tokens, expected):
            self.assertEqual(token.type, expected)

    def test_doubleCharacter(self):
        expected = [
            TokenType.EQUAL,
            TokenType.EQUAL_EQUAL,
            TokenType.MINUS,
            TokenType.LESS_EQUAL,
            TokenType.EQUAL,
            TokenType.GREATER,
            TokenType.EOF,
        ]

        scanner = Scanner("= == - <= =>", self.errorHandler)
        tokens = scanner.scanTokens()
        for token, expected in zip(tokens, expected):
            self.assertEqual(token.type, expected)

    def test_error(self):
        scanner = Scanner("@", self.errorHandler)
        tokens = scanner.scanTokens()
        self.errorHandler.error.assert_called_once_with(1, "@ Unexpected character.")

        self.errorHandler.error = MagicMock()
        scanner = Scanner("+\n@", self.errorHandler)
        tokens = scanner.scanTokens()
        self.errorHandler.error.assert_called_once_with(2, "@ Unexpected character.")

    def test_slash(self):
        expected = [TokenType.SLASH, TokenType.MINUS, TokenType.EOF]
        scanner = Scanner("/ -", self.errorHandler)
        tokens = scanner.scanTokens()
        for token, expected in zip(tokens, expected):
            self.assertEqual(token.type, expected)

    def test_comment(self):
        scanner = Scanner("//@ this is a comment", self.errorHandler)
        tokens = scanner.scanTokens()
        self.errorHandler.error.assert_not_called()

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)

    def test_multiLineComment(self):
        scanner = Scanner("//@ this is a comment\n+", self.errorHandler)
        tokens = scanner.scanTokens()
        self.errorHandler.error.assert_not_called()

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.PLUS)
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_string(self):
        scanner = Scanner('"Hello"', self.errorHandler)
        tokens = scanner.scanTokens()
        self.assertEqual(tokens[0].literal, "Hello")
        self.assertEqual(tokens[0].lexeme, '"Hello"')

        scanner = Scanner('"Unterminated string', self.errorHandler)
        tokens = scanner.scanTokens()
        self.errorHandler.error.assert_called_once_with(1, "Unterminated string")

    def test_number(self):
        scanner = Scanner("12.34/1", self.errorHandler)
        tokens = scanner.scanTokens()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertAlmostEqual(tokens[0].literal, 12.34)
        self.assertEqual(tokens[0].lexeme, "12.34")

        self.assertEqual(tokens[1].type, TokenType.SLASH)
        self.assertEqual(tokens[1].lexeme, "/")

        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertAlmostEqual(tokens[2].literal, 1)
        self.assertEqual(tokens[2].lexeme, "1")

    def test_identifiers(self):
        scanner = Scanner("varfun", self.errorHandler)
        tokens = scanner.scanTokens()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)

        scanner = Scanner("var", self.errorHandler)
        tokens = scanner.scanTokens()
        self.assertEqual(tokens[0].type, TokenType.VAR)

        scanner = Scanner("var fun", self.errorHandler)
        tokens = scanner.scanTokens()
        self.assertEqual(tokens[0].type, TokenType.VAR)
        self.assertEqual(tokens[1].type, TokenType.FUN)

    def test_multilineWithComments(self):
        expected = [
            TokenType.VAR,
            TokenType.IDENTIFIER,
            TokenType.EQUAL,
            TokenType.NUMBER,
            TokenType.VAR,
            TokenType.IDENTIFIER,
            TokenType.EQUAL,
            TokenType.STRING,
            TokenType.EOF,
        ]
        scanner = Scanner(
            'var x = 2 //This is a comment\nvar s = "Hello"', self.errorHandler
        )
        tokens = scanner.scanTokens()
        self.assertEqual(len(tokens), 9)

        for token, expected in zip(tokens, expected):
            self.assertEqual(token.type, expected)

        self.assertEqual(tokens[3].literal, 2)
        self.assertEqual(tokens[7].literal, "Hello")


if __name__ == "__main__":
    unittest.main()
