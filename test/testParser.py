import unittest
from unittest.mock import patch

from pylox.parser import Parser
from pylox.errorHandler import ErrorHandler
from pylox.scanner import Scanner

from pylox.parser import Parser


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.errorHandler = ErrorHandler

    def test_primary(self):
        scanner = Scanner("1", self.errorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        self.assertEqual(ast.value, 1)

    def test_binary(self):
        scanner = Scanner("1 - -2", self.errorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        self.assertEqual(ast.left.value, 1)
        self.assertEqual(ast.right.right.value, 2)

    def test_grouping(self):
        scanner = Scanner("(2)", self.errorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        self.assertEqual(ast.expr.value, 2)

    def test_greater(self):
        scanner = Scanner("2 > 2", self.errorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        self.assertEqual(ast.left.value, 2)
        self.assertEqual(ast.right.value, 2)


if __name__ == "__main__":
    unittest.main()
