from abc import ABC
from abc import abstractmethod

class ExprVisitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, stmt):
        pass

    @abstractmethod
    def visitGroupingExpr(self, stmt):
        pass

    @abstractmethod
    def visitLiteralExpr(self, stmt):
        pass

    @abstractmethod
    def visitUnaryExpr(self, stmt):
        pass

    @abstractmethod
    def visitVariableExpr(self, stmt):
        pass

