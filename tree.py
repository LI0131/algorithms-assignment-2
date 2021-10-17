import logging

import settings

from typing import List, Union, Tuple
from dataclasses import dataclass, field

from rational import Rational
from function import FunctionTypes, PolynomialFunction

app_logger = logging.getLogger(settings.APP_NAME)


@dataclass
class Node:
    size: str
    c: Union[Rational, str]
    op: FunctionTypes
    denominator: Union[Rational, int]
    power: Union[Rational, int]

    @property
    def cost(self):
        return f'{self.c}(n{self.op.value}{self.denominator})^{self.power}'

    @classmethod
    def from_func(cls, func: PolynomialFunction, layer: int):
        recursive_den: int = (func.b * 2 * layer) ** func.d
        app_logger.debug(f'Generating node for layer: {layer}')
        app_logger.debug(f'Denominator of recursive size: {func.b} ** {layer} = {func.b ** layer}')
        return cls(
            f'T(n{func.op.value}{func.b ** layer})',
            func.c, func.op, recursive_den, func.d
        )

    def __repr__(self):
        return f'[{self.size}, Cost: {self.cost}]'


@dataclass
class Tree:
    head: Tuple[Union[Node, None], str] = field(default_factory=tuple)
    layer1: Tuple[List[Node], str] = field(default_factory=tuple)
    layer2: Tuple[List[Node], str] = field(default_factory=tuple)
    layer3: Tuple[List[Node], str] = field(default_factory=tuple)

    def _compute_total_cost(self, layer: List[Node]):
        num_nodes: int = len(layer)
        app_logger.debug(f'Num nodes in layer: {num_nodes}')
        if num_nodes > 1:
            head: Node = layer[0]
            denominator: int = Rational(f'{head.denominator}') ** head.power
            frac: Rational = Rational(f'{num_nodes}/{denominator}')
            frac.reduce()
            return f'({frac}){head.cost}'
        elif num_nodes == 1:
            return layer[0].cost

    def get_layer(self, layer: int):
        if layer == 0:
            return self.head
        elif layer == 1:
            return self.layer1
        elif layer == 2:
            return self.layer2
        else:
            return self.layer3

    def append(self, data: List[Node], layer: int):
        if layer == 0:
            self.head = list(self.head)
            self.head.append(data)
            self.head.append(self._compute_total_cost(data))
            self.head = tuple(self.head)
        elif layer == 1:
            self.layer1 = list(self.layer1)
            self.layer1.append(data)
            self.layer1.append(self._compute_total_cost(data))
            self.layer1 = tuple(self.layer1)
        elif layer == 2:
            self.layer2 = list(self.layer2)
            self.layer2.append(data)
            self.layer2.append(self._compute_total_cost(data))
            self.layer2 = tuple(self.layer2)
        else:
            self.layer3 = list(self.layer3)
            self.layer3.append(data)
            self.layer3.append(self._compute_total_cost(data))
            self.layer3 = tuple(self.layer3)

    def __repr__(self):
        return f'\n-- HEAD --\n' + str(self.head) + '\n' + \
               f'-- Layer 1 --' + '\n' + \
               f'-- Total cost: {self.layer1[1]} --' + '\n' + \
               f'{str(self.layer1[0])}' + '\n' + \
               f'-- Layer 2 --' + '\n' + \
               f'-- Total cost: {self.layer2[1]} --' + '\n' + \
               f'{str(self.layer2[0])}' + '\n' + \
               f'-- Layer 3 --' + '\n' + \
               f'-- Total cost: {self.layer3[1]} --' + '\n' + \
               f'{str(self.layer3[0])}' + '\n'
