from pylox.token import TokenType
import pylox.Expr as Expr


class parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def match(self, *args):
        for token in args:
            if self.check(token):
                self.advance()
                return True

        return False

    def check(self, tokenType):
        if self.isAtEnd():
            return False
        else:
            return self.peek().type == tokenType

    def previous(self):
        return self.tokens[self.current - 1]

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def consume(self, tokenType, message):
        if self.check(tokenType):
            return self.advance()
        else:
            from pylox.lox import error

            error(self.peek(), message)

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term
            expr = Expr.Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.NUMBER):
            return Expr.Literal(self.previous().literal)

        if self.match(TokenType.STRING):
            return Expr.Literal(self.previous().literal)

        if self.match(TokenType.TRUE):
            return Expr.Literal(True)

        if self.match(TokenType.FALSE):
            return Expr.Literal(False)

        if self.match(TokenType.NIL):
            return Expr.Literal(None)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
