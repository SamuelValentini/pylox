class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        try:
            return self.values[name.lexeme]
        except KeyError:
            raise RuntimeError(name, f"Undefined variable {name.lexeme}.")
