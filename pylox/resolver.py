from ExprVisitor import ExprVisitor
from StmtVisitor import StmtVisitor


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter, errorHandler):
        self.interpreter = interpreter
        self.errorHandler = errorHandler
        self.scopes = []

    def visitBlockStmt(self, stmt):
        self.beginScope()
        self.resolveStatementList(stmt.statements)
        self.endScope()
        return None

    def visitVarStmt(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)

        self.define(stmt.name)

    def visitVariableExpr(self, expr):
        if not len(self.scopes) == 0 and self.scopes[-1][expr.name.lexeme] == False:
            self.errorHandler.error(
                expr.name, "Can't read local variable in its own initializer."
            )
        self.resolveLocal(expr, expr.name)
        return None

    def resolveStatementList(self, statements):
        for stmt in statements:
            self.resolve(stmt)

    def resolve(self, stmt):
        stmt.accept(self)

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def declare(self, name):
        if len(self.scopes) == 0:
            return None

        scope = self.scopes[-1]
        scope[name.lexeme] = False

    def define(self, name):
        if len(self.scopes) == 0:
            return None
        self.scopes[-1][name.lexeme] = True

    def resolveLocal(self, expr, name):
        for i, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, i)
