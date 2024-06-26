from abc import ABC
from abc import abstractmethod


class LoxCallable:
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass
