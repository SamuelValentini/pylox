from abc import ABC
from abc import abstractmethod

class Stmt:
    pass


class Expression(Stmt):

    def __init__(self, expression):
        self.expression = expression

    def accept(self,visitor):
        return visitor.visitExpressionStmt(self)


class Print(Stmt):

    def __init__(self, expression):
        self.expression = expression

    def accept(self,visitor):
        return visitor.visitPrintStmt(self)


class Var(Stmt):

    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self,visitor):
        return visitor.visitVarStmt(self)


class Block(Stmt):

    def __init__(self, statements):
        self.statements = statements

    def accept(self,visitor):
        return visitor.visitBlockStmt(self)


