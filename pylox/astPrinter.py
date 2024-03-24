import Expr
from visitor import Visitor
from token import TokenType
from token import Token


class AstPrinter(Visitor):
    def printExpr(self, expr):
        print(expr.accept(self))

    def paranthesize(self, name, expressions):
        builder = ["("]
        builder.append(name)
        for expr in expressions:
            builder.append(" ")
            builder.append(expr.accept(self))

        builder.append(")")

        return " ".join(builder)

    def visitBinaryExpr(self, expression):
        return self.paranthesize(
            expression.operator.lexeme, [expression.left, expression.right]
        )

    def visitGroupingExpr(self, expression):
        return self.paranthesize("group", expression.expression)

    def visitLiteralExpr(self, expression):
        if expression.value is None:
            return "nil"
        else:
            return str(expression.value)

    def visitUnaryExpr(self, expression):
        return self.paranthesize(expression.operator.lexeme, expression.right)


if __name__ == "__main__":
    expression = Expr.Binary(
        Expr.Literal(1),
        Token(TokenType.PLUS, "+", None, 1),
        Expr.Binary(
            Expr.Literal(5), Token(TokenType.SLASH, "/", None, 1), Expr.Literal(2)
        ),
    )
    printer = AstPrinter()
    printer.printExpr(expression)
