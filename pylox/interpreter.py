from Expr import Expr
from environment import Environment
from ExprVisitor import ExprVisitor
from StmtVisitor import StmtVisitor
from loxCallable import LoxCallable
from token import TokenType
from token import Token
from Return import ReturnValue

import time

from loxFunction import LoxFunction


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, errorHandler):
        self.errorHandler = errorHandler
        self.globals = Environment()
        self.environment = self.globals

        class Clock(LoxCallable):
            def arity(self):
                return 0

            def call(self, interpreter, arguments):
                return time.time()

            def __str__(self):
                return "<native fn>"

        self.globals.define("clock", Clock())

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            self.errorHandler.runtimeError(error)

    def stringify(self, object):
        if object is None:
            return "nil"
        elif isinstance(object, float):
            object = str(object)
            if object.endswith(".0"):
                return int(float(object))
            else:
                return object
        elif isinstance(object, bool):
            if object:
                return "true"
            else:
                return "false"
        else:
            return str(object)

    def execute(self, stmt):
        stmt.accept(self)

    def evaluate(self, expression):
        return expression.accept(self)

    def isTruthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return bool(value)
        return True

    def isEqual(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a is b

    def checkNumberOperand(self, operator, operand, other=1.0):
        # Hacky way! In this way you can use the same function
        # to check for both binary and unary operators
        if isinstance(operand, float) and isinstance(other, float):
            return
        raise RuntimeError(operator, "Operand must be a number")

    def visitBinaryExpr(self, expression):
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)
        match expression.operator.type:
            case TokenType.PLUS:
                if (isinstance(left, float) and isinstance(right, float)) or (
                    isinstance(left, str) and isinstance(right, str)
                ):
                    return left + right
                raise RuntimeError(
                    expression.operator, "Operands must be two numbers or two strings."
                )

            case TokenType.MINUS:
                self.checkNumberOperand(expression.operator, left, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self.checkNumberOperand(expression.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.checkNumberOperand(expression.operator, left, right)
                return float(left) * float(right)
            case TokenType.GREATER:
                self.checkNumberOperand(expression.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.checkNumberOperand(expression.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.checkNumberOperand(expression.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.checkNumberOperand(expression.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self.isEqual(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.isEqual(left, right)

        return None

    def visitLogicalExpr(self, expression):
        left = self.evaluate(expression.left)
        if expression.operator.type == TokenType.OR:
            if self.isTruthy(left):
                return left

        elif expression.operator.type == TokenType.AND:
            if not self.isTruthy(left):
                return left

        return self.evaluate(expression.right)

    def visitGroupingExpr(self, expression):
        return self.evaluate(expression.expr)

    def visitLiteralExpr(self, expression):
        return expression.value

    def visitUnaryExpr(self, expression):
        right = self.evaluate(expression.right)
        match expression.operator.type:
            case TokenType.BANG:
                return not self.isTruthy(right)
            case TokenType.MINUS:
                self.checkNumberOperand(expression.operator, right)
                return -float(right)

        return None

    def visitVariableExpr(self, expression):
        return self.environment.get(expression.name)

    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visitFunctionStmt(self, stmt):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visitReturnStmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise ReturnValue(value)

    def visitVarStmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitAssignmentExpr(self, expression):
        value = self.evaluate(expression.value)
        self.environment.assign(expression.name, value)
        return value

    def visitBlockStmt(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None

    def executeBlock(self, stmtList, environment):
        previousEnv = self.environment
        try:
            self.environment = environment
            for statement in stmtList:
                self.execute(statement)

        finally:
            self.environment = previousEnv

    def visitIfStmt(self, stmt):
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)

        return None

    def visitWhileStmt(self, stmt):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

        return None

    def visitCallExpr(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")

        function = callee
        if len(arguments) != function.arity():
            raise RuntimeError(
                expr.paren,
                f"Expected {function.arity()} arguments but got {len(arguments)}.",
            )

        return function.call(self, arguments)


if __name__ == "__main__":
    expression = Expr.Binary(
        Expr.Literal(1.0),
        Token(TokenType.PLUS, "+", None, 1),
        Expr.Binary(
            Expr.Literal(5.0), Token(TokenType.SLASH, "/", None, 1), Expr.Literal(2.0)
        ),
    )

    expression = Expr.Binary(
        Expr.Literal("HELLO"),
        Token(TokenType.GREATER, "-", None, 1),
        Expr.Literal("WORLD"),
    )

    expression = Expr.Unary(Token(TokenType.MINUS, "-", None, 1), Expr.Literal("HELLO"))

    printer = Interpreter()
    print(printer.evaluate(expression))
