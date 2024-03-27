import unittest
from unittest.mock import patch

from pylox.parser import Parser
from pylox.errorHandler import ErrorHandler
from pylox.scanner import Scanner
from pylox.interpreter import Interpreter


class TestInterpreter(unittest.TestCase):
    def setUp(self) -> None:
        self.errorHandler = ErrorHandler
        self.interpreter = Interpreter(self.errorHandler)

    def test_primary(self):
        scanner = Scanner("1", self.errorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        result = self.interpreter.interpret(ast)
        self.assertEqual(result, 1)

    def test_equality(self):
        scanner = Scanner("1 == 1", self.errorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        result = self.interpreter.interpret(ast)
        self.assertTrue(result)

    def test_subtraction(self):
        scanner = Scanner("1 - -1", self.errorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        result = self.interpreter.interpret(ast)
        self.assertEqual(result, 2)

    def test_not_equal(self):
        scanner = Scanner("1 != 1", self.errorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        result = self.interpreter.interpret(ast)
        self.assertFalse(result)

    def test_greaterThan(self):
        scanner = Scanner("2 > 1", self.errorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        result = self.interpreter.interpret(ast)
        self.assertTrue(result)

    def test_grouping(self):
        scanner = Scanner("(1 + 2) * 2", self.errorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        result = self.interpreter.interpret(ast)
        self.assertEqual(result, 6)

    def testStringConcat(self):
        scanner = Scanner(
            '"Hello world!" == ("Hello" + " " + "world") + "!" ', self.errorHandler
        )
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.errorHandler)
        ast = parser.parse()
        result = self.interpreter.interpret(ast)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
