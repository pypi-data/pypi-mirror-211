from dto import Expression, OneArgExpression, TwoArgsExpression
from calculator import OneArgCalculator, TwoArgsCalculator
from contracts import Calculator


def get_calculator(expression: Expression) -> Calculator:
    if isinstance(expression, OneArgExpression):
        return OneArgCalculator(expression)
    if isinstance(expression, TwoArgsExpression):
        return TwoArgsCalculator(expression)
    raise Exception("invalid expression")
