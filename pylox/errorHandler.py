class ErrorHandler:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print(f"[{line}] Error {where}: {message}")
        self.hadError = True

    def runtimeError(self, error):
        operator, message = error.args
        print(f"{message} \n[line {operator.line}]")
        self.hadRuntimeError = True
