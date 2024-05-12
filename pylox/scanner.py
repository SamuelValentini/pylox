from token import TokenType
from token import Token


class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source, errorHandler):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.errorHandler = errorHandler

    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens

    def scanToken(self):
        c = self.advance()
        match c:
            # Single Character Lexemes
            case "(":
                self.addToken(TokenType.LEFT_PAREN)
            case ")":
                self.addToken(TokenType.RIGHT_PAREN)
            case "{":
                self.addToken(TokenType.LEFT_BRACE)
            case "}":
                self.addToken(TokenType.RIGHT_BRACE)
            case ",":
                self.addToken(TokenType.COMMA)
            case ".":
                self.addToken(TokenType.DOT)
            case "-":
                self.addToken(TokenType.MINUS)
            case "+":
                self.addToken(TokenType.PLUS)
            case ";":
                self.addToken(TokenType.SEMICOLON)
            case "*":
                self.addToken(TokenType.STAR)

            # Double Character Lexemes
            case "!":
                self.addToken(TokenType.BANG_EQUAL) if self.match(
                    "="
                ) else self.addToken(TokenType.BANG)
            case "=":
                self.addToken(TokenType.EQUAL_EQUAL) if self.match(
                    "="
                ) else self.addToken(TokenType.EQUAL)
            case "<":
                self.addToken(TokenType.LESS_EQUAL) if self.match(
                    "="
                ) else self.addToken(TokenType.LESS)
            case ">":
                self.addToken(TokenType.GREATER_EQUAL) if self.match(
                    "="
                ) else self.addToken(TokenType.GREATER)

            # / and Comments
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and (not self.isAtEnd()):
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)

            # Remove with spaces
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.line += 1

            # Strings
            case '"':
                self.string()

            # Manage Errors
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha() or c == "_":
                    self.identifier()
                else:
                    # Ugly but it breaks the circular dependency
                    self.errorHandler.error(self.line, f"{c} Unexpected character.")

    def match(self, c):
        if self.isAtEnd():
            return False

        if self.source[self.current] != c:
            return False

        self.current += 1
        return True

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def peek(self):
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def string(self):
        while (self.peek() != '"') and (not self.isAtEnd()):
            if self.peek() == "\n":
                self.line += 1

            self.advance()

        if self.isAtEnd():
            self.errorHandler.error(self.line, "Unterminated string")
            return None

        # Closing
        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.addToken(TokenType.STRING, literal=value)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peekNext().isdigit():
            self.advance()

        while self.peek().isdigit():
            self.advance()

        value = float(self.source[self.start : self.current])
        self.addToken(TokenType.NUMBER, literal=value)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        text = self.source[self.start : self.current]
        if text in self.keywords:
            tokenType = self.keywords[text]
        else:
            tokenType = TokenType.IDENTIFIER

        self.addToken(tokenType)

    def addToken(self, type, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))
