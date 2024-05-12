from abc import ABC
from abc import abstractmethod

class ExprVisitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr):
        pass

    @abstractmethod
    def visitCallExpr(self, expr):
        pass

    @abstractmethod
    def visitGetExpr(self, expr):
        pass

    @abstractmethod
    def visitGroupingExpr(self, expr):
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr):
        pass

    @abstractmethod
    def visitLogicalExpr(self, expr):
        pass

    @abstractmethod
    def visitSetExpr(self, expr):
        pass

    @abstractmethod
    def visitSuperExpr(self, expr):
        pass

    @abstractmethod
    def visitThisExpr(self, expr):
        pass

    @abstractmethod
    def visitUnaryExpr(self, expr):
        pass

    @abstractmethod
    def visitVariableExpr(self, expr):
        pass

    @abstractmethod
    def visitAssignmentExpr(self, expr):
        pass

