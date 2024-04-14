from abc import ABC
from abc import abstractmethod


class LoxCallable:
    @property
    def arity(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass
