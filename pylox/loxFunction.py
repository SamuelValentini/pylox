from loxCallable import LoxCallable
from environment import Environment


class LoxFunction(LoxCallable):
    def __init__(self, declaration):
        self.declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for decl, arg in zip(self.declaration.params, arguments):
            environment.define(decl.lexeme, arg)

        interpreter.executeBlock(self.declaration.body, environment)
        return None

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
