from token import TokenType
from token import Token
import lox

class Scanner():

    def __init__(self,source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanTokens(self):

        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()

        self.tokens.append( Token( TokenType.EOF, "", self.line ))

    def scanToken(self):
        c = self.advance()
        match c:
            case '(':
                self.addToken(TokenType.LEFT_PAREN)
            case ')':
                self.addToken(TokenType.RIGHT_PAREN)
            case '{':
                self.addToken(TokenType.LEFT_BRACE)
            case '}':
                self.addToken(TokenType.RIGHT_BRACE)
            case ',':
                self.addToken(TokenType.COMMA)
            case '.':
                self.addToken(TokenType.DOT)
            case '-':
                self.addToken(TokenType.MINUS)
            case '+':
                self.addToken(TokenType.PLUS)
            case ';':
                self.addToken(TokenType.SEMICOLON)
            case '*':
                self.addToken(TokenType.STAR)

            case _:
                lox.error(self.line, "Unexpected character.")


    def advance(self):
        self.current += 1
        return self.source[self.current-1]

    def addToken(self,type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
