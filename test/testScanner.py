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

if __name__ == '__main__':
    unittest.main()
