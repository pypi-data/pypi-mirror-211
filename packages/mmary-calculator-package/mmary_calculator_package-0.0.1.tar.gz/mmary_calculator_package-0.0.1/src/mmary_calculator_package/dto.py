from custom_types import Number
from enums import Operation

from abc import ABC


class Expression(ABC):
    pass


class OneArgExpression(Expression):
    def __init__(self, arg: Number, operation: Operation) -> None:
        super().__init__()
        self.__argument = arg
        self.__operation = operation
    
    @property
    def argument(self) -> Number:
        return self.__argument

    @property
    def operation(self) -> Operation:
        return self.__operation


class TwoArgsExpression(Expression):
    def __init__(
        self, 
        first_arg: Number, 
        second_arg: Number, 
        operation: Operation
    ) -> None:
        super().__init__()
        self.__first_arg = first_arg
        self.__second_arg = second_arg
        self.__operation = operation
    
    @property
    def first_argument(self) -> Number:
        return self.__first_arg

    @property
    def second_argument(self) -> Number:
        return self.__second_arg
    
    @property
    def operation(self) -> Operation:
        return self.__operation
