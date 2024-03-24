from abc import ABC
from abc import abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, expression):
        pass

    @abstractmethod
    def visitGroupingExpr(self, expression):
        pass

    @abstractmethod
    def visitLiteralExpr(self, expression):
        pass

    @abstractmethod
    def visitUnaryExpr(self, expression):
        pass

