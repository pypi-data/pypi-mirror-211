from dto import OneArgExpression, TwoArgsExpression
from contracts import Calculator
from custom_types import Number
from enums import Operation

from math import (
    sin as math_sin,
    cos as math_cos,
    tan as math_tan,
)


class OneArgCalculator(Calculator):
    def __init__(self, expression: OneArgExpression) -> None:
        super().__init__()
        self.__expression = expression
    
    def calculate(self) -> Number:
        match self.__expression.operation:
            case Operation.SIN:
                return self._sin(self.__expression.argument)
            case Operation.COS:
                return self._cos(self.__expression.argument)
            case Operation.TAN:
                return self._tan(self.__expression.argument)
            case Operation.COTAN:
                return self._cotan(self.__expression.argument)
        raise Exception("invalid operation")
        
    def _sin(self, n: Number) -> Number:
        return math_sin(n)

    def _cos(self, n: Number) -> Number:
        return math_cos(n)

    def _tan(self, n: Number) -> Number:
        return math_tan(n)
    
    def _cotan(self, n: Number) -> Number:
        return 1 / self.tan(n)


class TwoArgsCalculator(Calculator):
    def __init__(self, expression: TwoArgsExpression) -> None:
        super().__init__()
        self.__expression = expression
    
    def calculate(self) -> Number:
        match self.__expression.operation:
            case Operation.PLUS:
                return self._addition(
                    self.__expression.first_argument,
                    self.__expression.second_argument
                )
            case Operation.MINUS:
                return self._subtraction(
                    self.__expression.first_argument,
                    self.__expression.second_argument
                )
            case Operation.MULTI:
                return self._multiplication(
                    self.__expression.first_argument,
                    self.__expression.second_argument
                )
            case Operation.DIV:
                return self._division(
                    self.__expression.first_argument,
                    self.__expression.second_argument
                )
            case Operation.EXP:
                return self._exponentiation(
                    self.__expression.first_argument,
                    self.__expression.second_argument
                )
            case Operation.ROOT_POWER:
                return self._power_root(
                    self.__expression.first_argument,
                    self.__expression.second_argument
                )
        raise Exception("invalid operation")

    def _addition(self, n1: Number, n2: Number) -> Number:
        return n1 + n2

    def _subtraction(self, n1: Number, n2: Number) -> Number:
        return n1 - n2

    def _multiplication(self, n1: Number, n2: Number) -> Number:
        return n1 * n2
    
    def _division(self, n1: Number, n2: Number) -> Number:
        return n1 / n2

    def _exponentiation(self, n: Number, power: Number) -> Number:
        return n ** power

    def _power_root(self, n: Number, power: Number) -> Number:
        return n ** (1 / power)
