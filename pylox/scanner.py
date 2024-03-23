from pylox.token import TokenType
from pylox.token import Token

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

        self.tokens.append( Token( TokenType.EOF, "", None, self.line ))

        return self.tokens

    def scanToken(self):
        c = self.advance()
        match c:
            #Single Character Lexemes
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

            #Double Character Lexemes
            case '!':
                self.addToken(TokenType.BANG_EQUAL) if self.match('=') else self.addToken(TokenType.BANG)
            case '=':
                self.addToken(TokenType.EQUAL_EQUAL) if self.match('=') else self.addToken(TokenType.EQUAL)
            case '<':
                self.addToken(TokenType.LESS_EQUAL) if self.match('=') else self.addToken(TokenType.LESS)
            case '>':
                self.addToken(TokenType.GREATER_EQUAL) if self.match('=') else self.addToken(TokenType.GREATER)

            #/ and Comments
            case '/':
                if self.match('/'):
                    while(self.peek() != '\n' and (not self.isAtEnd)):
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)

            #Remove with spaces
            case ' ':
                pass
            case '\r':
                pass
            case '\t':
                pass
            case '\n':
                self.line += 1

            #Strings
            case '"':
                self.string()

            #Manage Errors
            case _:
                #Ugly but it breaks the circular dependency
                from pylox.lox import error
                error(self.line, f"{c} Unexpected character.")


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
            return '\0'
        return self.source[self.current]

    def string(self):
        while(self.peek() != '"') and (not self.isAtEnd()):
            if self.peek() == '\n':
                self.line += 1

            self.advance()

        value = self.source[self.start + 1:self.current]
        self.addToken(TokenType.STRING, literal=value)

    def addToken(self,type, literal=None):
        text = self.source[self.start:self.current+1]
        self.tokens.append(Token(type, text, literal, self.line))

