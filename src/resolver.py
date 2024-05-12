from ExprVisitor import ExprVisitor
from StmtVisitor import StmtVisitor
from enum import Enum
from enum import auto

from LoxInstance import LoxInstance


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    INITIALIZER = auto()
    METHOD = auto()


class ClassType(Enum):
    NONE = auto()
    CLASS = auto()
    SUBCLASS = auto()


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter, errorHandler):
        self.interpreter = interpreter
        self.errorHandler = errorHandler
        self.scopes = []
        self.currentFunction = FunctionType.NONE
        self.currentClass = ClassType.NONE

    def visitBlockStmt(self, stmt):
        self.beginScope()
        self.resolve(stmt.statements)
        self.endScope()
        return None

    def visitClassStmt(self, stmt):
        enclosingClass = self.currentClass
        self.currentClass = ClassType.CLASS
        self.declare(stmt.name)
        self.define(stmt.name)

        if (
            stmt.superclass is not None
            and stmt.name.lexeme == stmt.superclass.name.lexeme
        ):
            self.errorHandler.error(
                stmt.superclass.name.line, "A class can't inherit from itself"
            )

        if stmt.superclass is not None:
            self.currentClass = ClassType.SUBCLASS
            self.resolve(stmt.superclass)
            self.beginScope()
            self.scopes[-1]["super"] = True

        self.beginScope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            self.resolveFunction(method, declaration)

        self.endScope()

        if stmt.superclass is not None:
            self.endScope()

        self.currentClass = enclosingClass

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
            self.errorHandler.error(
                stmt.keyword.line, "Can't return from top-level code."
            )

        if stmt.value is not None:
            if self.currentFunction == FunctionType.INITIALIZER:
                self.errorHandler.error(
                    stmt.keyword.line, "Can't return a value from an initializer."
                )
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

    def visitGetExpr(self, expr):
        self.resolve(expr.obj)
        return None

    def visitGroupingExpr(self, expr):
        self.resolve(expr.expr)
        return None

    def visitLiteralExpr(self, expr):
        return None

    def visitLogicalExpr(self, expr):
        self.resolve(expr.right)
        return None

    def visitSetExpr(self, expr):
        self.resolve(expr.value)
        self.resolve(expr.obj)
        return None

    def visitSuperExpr(self, expr):
        if self.currentClass == ClassType.NONE:
            self.errorHandler.error(
                expr.keyword.line, "Can't use 'super' outside of a class."
            )
        elif self.currentClass != ClassType.SUBCLASS:
            self.errorHandler.error(
                expr.keyword.line, "Can't use 'super' in a class with no superclass."
            )
        self.resolveLocal(expr, expr.keyword)
        return None

    def visitThisExpr(self, expr):
        if self.currentClass == ClassType.NONE:
            self.errorHandler.error(
                expr.keyword.line, "Can't use 'this' outside of a class."
            )
            return None
        self.resolveLocal(expr, expr.keyword)
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

    def resolveFunction(self, function, type):
        enclosingFunction = self.currentFunction
        self.currentFunction = type
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
