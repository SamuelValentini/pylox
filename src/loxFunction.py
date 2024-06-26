from loxCallable import LoxCallable
from environment import Environment
from Return import ReturnValue


class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, isInitializer):
        self.isInitializer = isInitializer
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for decl, arg in zip(self.declaration.params, arguments):
            environment.define(decl.lexeme, arg)

        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except ReturnValue as r:
            if self.isInitializer:
                return self.closure.getAt(0, "this")
            return r.value

        if self.isInitializer:
            return self.closure.getAt(0, "this")
        return None

    def arity(self):
        return len(self.declaration.params)

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.isInitializer)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
