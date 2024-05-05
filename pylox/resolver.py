from ExprVisitor import ExprVisitor
from StmtVisitor import StmtVisitor
from enum import Enum
from enum import auto

from pylox.errorHandler import ErrorHandler


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter, errorHandler):
        self.interpreter = interpreter
        self.errorHandler = errorHandler
        self.scopes = []
        self.currentFunction = FunctionType.NONE

    def visitBlockStmt(self, stmt):
        self.beginScope()
        self.resolve(stmt.statements)
        self.endScope()
        return None

    def visitExpressionStmt(self, stmt):
        self.resolve(stmt.expression)
        return None

    def visitIfStmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch is not None:
            self.resolve(stmt.elseBranch)
        return None

    def visitPrintStmt(self, stmt):
        self.resolve(stmt.expression)
        return None

    def visitReturnStmt(self, stmt):
        if self.currentFunction == FunctionType.NONE:
            self.errorHandler.error(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            self.resolve(stmt.value)
        return None

    def visitWhileStmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
        return None

    def visitFunctionStmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolveFunction(stmt, FunctionType.FUNCTION)
        return None

    def visitVarStmt(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)

        self.define(stmt.name)
        return None

    def visitAssignmentExpr(self, expr):
        self.resolve(expr.value)
        self.resolveLocal(expr, expr.name)
        return None

    def visitVariableExpr(self, expr):
        if not len(self.scopes) == 0 and self.scopes[-1].get(expr.name.lexeme) == False:
            self.errorHandler.error(
                expr.name, "Can't read local variable in its own initializer."
            )
        self.resolveLocal(expr, expr.name)
        return None

    def visitBinaryExpr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visitCallExpr(self, expr):
        self.resolve(expr.callee)

        for argument in expr.arguments:
            self.resolve(argument)
        return None

    def visitGroupingExpr(self, expr):
        self.resolve(expr.expression)
        return None

    def visitLiteralExpr(self, expr):
        return None

    def visitLogicalExpr(self, expr):
        self.resolve(expr.right)
        return None

    def visitUnaryExpr(self, expr):
        self.resolve(expr.right)
        return None

    def resolve(self, stmt):
        if isinstance(stmt, list):
            for s in stmt:
                self.resolve(s)
        else:
            stmt.accept(self)

    def resolveFunction(self, function, type_):
        enclosingFunction = self.currentFunction
        self.currentFunction = type_
        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.endScope()
        self.currentFunction = enclosingFunction

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def declare(self, name):
        if len(self.scopes) == 0:
            return None

        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.errorHandler.error(
                name, "Already variable with this name in this scope"
            )
        scope[name.lexeme] = False

    def define(self, name):
        if len(self.scopes) == 0:
            return None
        self.scopes[-1][name.lexeme] = True

    def resolveLocal(self, expr, name):
        for i, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, i)
                return None
