from abc import ABC
from abc import abstractmethod

class Expr:
    pass


class Binary(Expr):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self,visitor):
        return visitor.visitBinaryExpr(self)


class Call(Expr):

    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self,visitor):
        return visitor.visitCallExpr(self)


class Grouping(Expr):

    def __init__(self, expr):
        self.expr = expr

    def accept(self,visitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):

    def __init__(self, value):
        self.value = value

    def accept(self,visitor):
        return visitor.visitLiteralExpr(self)


class Logical(Expr):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self,visitor):
        return visitor.visitLogicalExpr(self)


class Unary(Expr):

    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self,visitor):
        return visitor.visitUnaryExpr(self)


class Variable(Expr):

    def __init__(self, name):
        self.name = name

    def accept(self,visitor):
        return visitor.visitVariableExpr(self)


class Assignment(Expr):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self,visitor):
        return visitor.visitAssignmentExpr(self)


