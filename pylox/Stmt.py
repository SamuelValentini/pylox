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


