from abc import ABC
from abc import abstractmethod

class StmtVisitor(ABC):
    @abstractmethod
    def visitExpressionStmt(self, stmt):
        pass

    @abstractmethod
    def visitPrintStmt(self, stmt):
        pass

    @abstractmethod
    def visitVarStmt(self, stmt):
        pass

