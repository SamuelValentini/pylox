from os import environ
import Expr as Expr
from environment import Environment
from ExprVisitor import ExprVisitor
from StmtVisitor import StmtVisitor
from loxCallable import LoxCallable
from token import TokenType
from token import Token
from LoxClass import LoxClass
from Return import ReturnValue

import time

from loxFunction import LoxFunction
from LoxInstance import LoxInstance


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, errorHandler):
        self.errorHandler = errorHandler
        self.globals = Environment()
        self.environment = self.globals
        self.locals = {}

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
        elif isinstance(object, list):
            return str([self.stringify(x) for x in object])
        else:
            return str(object)

    def execute(self, stmt):
        stmt.accept(self)

    def resolve(self, expr, depth):
        self.locals[expr] = depth

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
        return a == b

    def checkNumberOperand(self, operator, operand, other=1.0):
        # Hacky way! In this way you can use the same function
        # to check for both binary and unary operators
        if isinstance(operand, float) and isinstance(other, float):
            return
        raise RuntimeError(operator, "Operand must be a number")

    def visitBinaryExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.PLUS:
                if (isinstance(left, float) and isinstance(right, float)) or (
                    isinstance(left, str) and isinstance(right, str)
                ):
                    return left + right
                raise RuntimeError(
                    expr.operator, "Operands must be two numbers or two strings."
                )

            case TokenType.MINUS:
                self.checkNumberOperand(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self.checkNumberOperand(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.checkNumberOperand(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.GREATER:
                self.checkNumberOperand(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.checkNumberOperand(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.checkNumberOperand(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.checkNumberOperand(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self.isEqual(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.isEqual(left, right)

        return None

    def visitLogicalExpr(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self.isTruthy(left):
                return left

        elif expr.operator.type == TokenType.AND:
            if not self.isTruthy(left):
                return left

        return self.evaluate(expr.right)

    def visitSetExpr(self, expr):
        obj = self.evaluate(expr.obj)
        if not isinstance(obj, LoxInstance):
            raise RuntimeError(expr.name, "Only instances have fields.")

        value = self.evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    def visitThisExpr(self, expr):
        return self.lookUpVariable(expr.keyword, expr)

    def visitGroupingExpr(self, expr):
        return self.evaluate(expr.expr)

    def visitLiteralExpr(self, expr):
        return expr.value

    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.BANG:
                return not self.isTruthy(right)
            case TokenType.MINUS:
                self.checkNumberOperand(expr.operator, right)
                return -float(right)

        return None

    def visitVariableExpr(self, expr):
        pos = None
        if expr.pos is not None:
            try:
                pos = int(self.evaluate(expr.pos))
            except ValueError:
                raise RuntimeError(
                    expr.name, "Array position must evaluate to integers."
                )

        return self.lookUpVariable(expr.name, expr, pos)

    def lookUpVariable(self, name, expr, pos=None):
        try:
            distance = self.locals[expr]
            return self.environment.getAt(distance, name.lexeme, pos)
        except KeyError:
            return self.globals.get(name, pos)

    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visitFunctionStmt(self, stmt):
        function = LoxFunction(stmt, self.environment, False)
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
        length = 0
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        if stmt.length is not None:
            try:
                length = int(self.evaluate(stmt.length))
            except TypeError:
                raise RuntimeError(length, "Array position must evaluate to integers.")

        if length == 0:
            self.environment.define(stmt.name.lexeme, value)
        else:
            self.environment.define(stmt.name.lexeme, [value] * length)

        return None

    def visitAssignmentExpr(self, expr):
        value = self.evaluate(expr.value)
        pos = None
        if expr.pos is not None:
            try:
                pos = int(self.evaluate(expr.pos))
            except TypeError:
                raise RuntimeError(length, "Array position must evaluate to integers.")
        try:
            distance = self.locals[expr]
            self.environment.assignAt(distance, expr.name, value, pos)
        except KeyError:
            self.globals.assign(expr.name, value, pos)

        return value

    def visitBlockStmt(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None

    def visitClassStmt(self, stmt):
        superclass = None

        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise RuntimeError(stmt.superclass.name, "Superclass must be a class.")

        self.environment.define(stmt.name.lexeme, None)

        if stmt.superclass is not None:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)

        methods = {}
        for method in stmt.methods:
            function = LoxFunction(
                method, self.environment, method.name.lexeme == "init"
            )
            methods[method.name.lexeme] = function
        klass = LoxClass(stmt.name.lexeme, superclass, methods)

        if superclass is not None:
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name, klass)
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

    def visitGetExpr(self, expr):
        obj = self.evaluate(expr.obj)
        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)

        raise RuntimeError(
            expr.name,
            "Only instances have properties.",
        )

    def visitSuperExpr(self, expr):
        distance = self.locals[expr]
        superclass = self.environment.getAt(distance, "super")
        obj = self.environment.getAt(distance - 1, "this")

        method = superclass.findMethod(expr.method.lexeme)
        if method is None:
            raise RuntimeError(
                expr.method, f"Undefinied property '{expr.method.lexeme}'."
            )
        return method.bind(obj)
