from abc import ABC, abstractmethod
from custom_types import Number


class Calculator(ABC):
    @abstractmethod
    def calculate(self) -> Number: pass
