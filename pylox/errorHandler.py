class ErrorHandler:
    def __init__(self):
        self.hadError = False

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print(f"line: {line}] Error {where}: {message}")
        self.hadError = True
