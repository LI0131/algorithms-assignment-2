from __future__ import annotations

import math
import copy
import logging

import settings

from typing import Union
from dataclasses import dataclass

app_logger = logging.getLogger(settings.APP_NAME)


@dataclass(init=False)
class Rational:
    numerator: int
    denominator: int

    def __init__(self, value: str = '1'):
        if '/' in value:
            value = value.split('/')
            self.numerator = int(value[0])
            self.denominator = int(value[1])
        elif len(value) > 0:
            self.numerator = int(value)
            self.denominator = 1
        else:
            self.numerator = 1
            self.denominator = 1

    def __repr__(self):
        if self.numerator % self.denominator == 0:
            return f'{int(self.numerator/self.denominator)}'
        elif self.denominator == 1:
            return self.numerator
        else:
            return f'({self.numerator}/{self.denominator})'

    def __mul__(self, other: Union[Rational, int]):
        obj = self.copy()
        if type(other) is Rational:
            obj.numerator = obj.numerator * other.numerator
            obj.denominator = obj.denominator * other.denominator
        else:
            obj.numerator = obj.numerator * other
        obj.reduce()
        return obj

    def __pow__(self, other: Union[int, Rational]):
        obj = self.copy()
        if type(other) is int:
            app_logger.debug(f'Power is an integer: {other}')
            obj.numerator = obj.numerator ** other
            obj.denominator = obj.denominator ** other
            app_logger.debug(f'Results: {obj.numerator}/{obj.denominator}')
        else:
            other_value: float = other.numerator / other.denominator
            obj.numerator = int(obj.numerator ** other_value)
            obj.denominator = int(obj.denominator ** other_value)
        obj.reduce()
        return obj

    def copy(self):
        return copy.copy(self)

    def lcm(self, obj: Rational):
        lcm = (self.numerator * self.denominator) // math.gcd(abs(obj.denominator), obj.numerator)
        return lcm

    def reduce(self):
        if (self.numerator != 0):
            common: int = math.gcd(abs(self.denominator), self.numerator)
            self.numerator = self.numerator // common
            self.denominator = self.denominator // common


if __name__ == "__main__":
    rat = Rational('5/1')
    print(rat * Rational('1/2'))
