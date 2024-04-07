from token import TokenType
import Expr as Expr
import Stmt as Stmt


class ParseError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Parser:
    def __init__(self, tokens, errorHandler):
        self.tokens = tokens
        self.current = 0
        self.errorHandler = errorHandler

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
            self.error(self.peek(), message)

    def error(self, token, message):
        if token.type == TokenType.EOF:
            self.errorHandler.report(token.line, " at end", message)
        else:
            self.errorHandler.report(token.line, f" at ' {token.lexeme} ''", message)

        raise ParseError(message)

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return

            match self.peek().type:
                case TokenType.CLASS:
                    return None
                case TokenType.FUN:
                    return None
                case TokenType.VAR:
                    return None
                case TokenType.FOR:
                    return None
                case TokenType.IF:
                    return None
                case TokenType.WHILE:
                    return None
                case TokenType.PRINT:
                    return None
                case TokenType.RETURN:
                    return None

            self.advance()

    def parse(self):
        try:
            statements = []
            while not self.isAtEnd():
                statements.append(self.declaration())
            return statements
        except ParseError:
            return None

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
            right = self.term()
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

        if self.match(TokenType.IDENTIFIER):
            return Expr.Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

        self.error(self.peek(), "Expected expression.")

    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Stmt.Print(value)

    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Stmt.Expression(expr)

    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Stmt.Var(name, initializer)

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printStatement()
        return self.expressionStatement()
