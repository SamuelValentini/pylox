class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def ancestor(self, distance):
        i = 0
        environment = self
        while i < distance:
            environment = environment.enclosing
            i += 1

        return environment

    def getAt(self, distance, name, pos=None):
        if pos is None:
            return self.ancestor(distance).values[name]

        var = self.ancestor(distance).values[name]

        if not isinstance(var, list):
            raise RuntimeError(name, f"{name.lexeme} not an array.")
        elif pos < len(var):
            return self.ancestor(distance).values[pos]
        else:
            raise RuntimeError(name, f"Array out of bound {name.lexeme}.")

    def assignAt(self, distance, name, value):
        self.ancestor(distance).values[name.lexeme] = value

    def get(self, name, pos=None):
        if name.lexeme in self.values:
            if pos is None:
                return self.values[name.lexeme]
            else:
                var = self.values[name.lexeme]
                if not isinstance(var, list):
                    raise RuntimeError(name, f"{name.lexeme} not an array.")
                elif pos < len(var):
                    return var[pos]
                else:
                    raise RuntimeError(name, f"Array out of bound {name.lexeme}.")

        if self.enclosing is not None:
            return self.enclosing.get(name, pos)

        raise RuntimeError(name, f"Undefined variable {name.lexeme}.")

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return None

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return None

        raise RuntimeError(name, f"Undefined variable {name.lexeme}.")
