import Expr
from visitor import Visitor
from token import TokenType
from token import Token


class Interpreter(Visitor):
    def evaluate(self, expression):
        return expression.accept(self)

    def isTruthy(self, value):
        if value is None:
            return False
        return bool(value)

    def isEqual(a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def visitBinaryExpr(self, expression):
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)
        match expression.operator.type:
            case TokenType.PLUS:
                if (isinstance(left, float) and isinstance(right, float)) or (
                    isinstance(left, str) and isinstance(right, str)
                ):
                    return left + right

            case TokenType.MINUS:
                return float(left) - float(right)
            case TokenType.SLASH:
                return float(left) / float(right)
            case TokenType.STAR:
                return float(left) * float(right)
            case TokenType.GREATER:
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                return float(left) >= float(right)
            case TokenType.LESS:
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self.isEqual(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.isEqual(left, right)

        return None

    def visitGroupingExpr(self, expression):
        return self.evaluate(expression)

    def visitLiteralExpr(self, expression):
        return expression.value

    def visitUnaryExpr(self, expression):
        right = self.evaluate(expression.right)
        match expression.operator.type:
            case TokenType.BANG:
                return not self.isTruthy(right)
            case TokenType.MINUS:
                return -float(right)

        return None


if __name__ == "__main__":
    expression = Expr.Binary(
        Expr.Literal(1),
        Token(TokenType.PLUS, "+", None, 1),
        Expr.Binary(
            Expr.Literal(5), Token(TokenType.SLASH, "/", None, 1), Expr.Literal(2)
        ),
    )

    printer = Interpreter()
    print(printer.evaluate(expression))
