#!/usr/bin/python3
import sys
from scanner import Scanner
from parser import Parser
from resolver import Resolver
from interpreter import Interpreter
from errorHandler import ErrorHandler


class Lox:
    def __init__(self) -> None:
        self.errorHandler = ErrorHandler()
        self.interpreter = Interpreter(self.errorHandler)

    def main(self):
        if len(sys.argv) > 2:
            print("Usage: pylox [script]")
            quit()
        elif len(sys.argv) == 2:
            self.runFile(sys.argv[1])
        else:
            self.runPrompt()

    def runFile(self, path):
        with open(path) as f:
            program = "".join(f.readlines())

        self.run(program)

        if self.errorHandler.hadError:
            sys.exit(65)

        if self.errorHandler.hadRuntimeError:
            sys.exit(70)

    def runPrompt(self):
        while True:
            line = input("> ")
            if line == "":
                quit()
            self.run(line)
            self.errorHandler.hadError = False

    def run(self, source):
        scanner = Scanner(source, self.errorHandler)
        tokens = scanner.scanTokens()

        if self.errorHandler.hadError:
            return

        parser = Parser(tokens, self.errorHandler)
        statements = parser.parse()

        if self.errorHandler.hadError:
            return

        resolver = Resolver(self.interpreter, self.errorHandler)
        resolver.resolve(statements)

        if self.errorHandler.hadError:
            return

        self.interpreter.interpret(statements)


if __name__ == "__main__":
    lox = Lox()
    lox.main()
