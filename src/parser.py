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
            self.errorHandler.report(token.line, f" at '{token.lexeme}'", message)

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
        return self.assignment()

    def assignment(self):
        expr = self.orOp()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Expr.Variable):
                name = expr.name
                return Expr.Assignment(name, value)
            elif isinstance(expr, Expr.Get):
                get = expr
                return Expr.Set(get.obj, get.name, value)

            self.errorHandler.error(equals, "Invalid assignment target.")

        return expr

    def orOp(self):
        expr = self.andOp()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.andOp()
            expr = Expr.Logical(expr, operator, right)

        return expr

    def andOp(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)

        return expr

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

        return self.call()

    def call(self):
        expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finishCall(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(
                    TokenType.IDENTIFIER, "Expect property name after '.'."
                )
                expr = Expr.Get(expr, name)
            else:
                break

        return expr

    def finishCall(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())

        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments")

        return Expr.Call(callee, paren, arguments)

    def primary(self):
        if self.match(TokenType.NUMBER):
            return Expr.Literal(self.previous().literal)

        if self.match(TokenType.STRING):
            return Expr.Literal(self.previous().literal)

        if self.match(TokenType.SUPER):
            keyword = self.previous()
            self.consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self.consume(
                TokenType.IDENTIFIER, "Expect superclass method name."
            )
            return Expr.Super(keyword, method)

        if self.match(TokenType.TRUE):
            return Expr.Literal(True)

        if self.match(TokenType.FALSE):
            return Expr.Literal(False)

        if self.match(TokenType.NIL):
            return Expr.Literal(None)

        if self.match(TokenType.THIS):
            return Expr.This(self.previous())

        if self.match(TokenType.IDENTIFIER):
            var = self.previous()
            pos = None
            if self.match(TokenType.LEFT_BRACKET):
                pos = self.expression()
                self.consume(TokenType.RIGHT_BRACKET, "Expect ']' after array position")
            return Expr.Variable(var, pos)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

        self.error(self.peek(), "Expected expression.")

    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def returnStatement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Stmt.Return(keyword, value)

    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Expression(expr)

    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        lenght = None

        if self.match(TokenType.LEFT_BRACKET):
            lenght = self.expression()
            self.consume(TokenType.RIGHT_BRACKET, "Expect ']' after lenght")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Var(name, lenght, initializer)

    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(
                self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
            )
            while self.match(TokenType.COMMA):
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameter.")

                parameters.append(
                    self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
                )

        self.consume(TokenType.RIGHT_PAREN, f"Expect ')' before {kind} body.")

        self.consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.block()
        return Stmt.Function(name, parameters, body)

    def declaration(self):
        try:
            if self.match(TokenType.CLASS):
                return self.classDeclaration()
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def classDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect class name.")
        superclass = None
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER, "Expect superclass name")
            superclass = Expr.Variable(self.previous(), None)
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
        methods = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            methods.append(self.function("method"))

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")

        return Stmt.Class(name, superclass, methods)

    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after if.")
        expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")

        thenBranch = self.statement()
        elseBranch = None

        if self.match(TokenType.ELSE):
            elseBranch = self.statement()

        return Stmt.If(expr, thenBranch, elseBranch)

    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after if.")
        expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return Stmt.While(expr, body)

    def forStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after if.")
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.statement()

        if increment is not None:
            body = Stmt.Block([body, Stmt.Expression(increment)])

        if condition is None:
            condition = Expr.Literal(True)
        body = Stmt.While(condition, body)

        if initializer is not None:
            body = Stmt.Block([initializer, body])

        return body

    def statement(self):
        if self.match(TokenType.IF):
            return self.ifStatement()
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.RETURN):
            return self.returnStatement()
        if self.match(TokenType.WHILE):
            return self.whileStatement()
        if self.match(TokenType.FOR):
            return self.forStatement()
        if self.match(TokenType.LEFT_BRACE):
            return Stmt.Block(self.block())
        return self.expressionStatement()
