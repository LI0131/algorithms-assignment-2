import re
import logging

from enum import Enum
from typing import List, Union
from dataclasses import dataclass

from settings import APP_NAME
from rational import Rational


__all__ = ['get_function', 'PolynomialFunction']


REGEX_START = r'T\(n\)\s=\s'
DIVISION_REGEX = REGEX_START + r'\d?T\(n\/\d\)\s\+\s'
SUBTRACTION_REGEX = REGEX_START + r'\d?T\(n-\d\)\s\+\s'
POLYNOMIAL_FUNCTION_REGEX = r'\w?\/?\w?n\^?\d?\/?\d?'
CONSTANT_FUNCTION_REGEX = r'\w?\/?\w?\d*\^?\d?\/?\d?'
BIG_O_FUNCTION_REGEX = r'O\(n\^\d{1,}\/?\d*?\)'
THETA_FUNCTION_REGEX = r'Theta\(n\^?\d*?\/?\d*?\)'
OMEGA_FUNCTION_REGEX = r'Omega\(n\^\d{1,}\/?\d*?\)'


app_logger = logging.getLogger(APP_NAME)


class FunctionTypes(Enum):
    DIVISION = '/'
    SUBTRACTION = '-'


@dataclass(init=False)
class Function:
    a: int
    b: Rational
    op: FunctionTypes

    def __init__(self, func: str):
        # if the incoming function contains division in recursive definition
        if re.match(DIVISION_REGEX, func):
            app_logger.debug(f'Division expression found in incoming function')
            self._parse_division_expression(func)
            self.op = FunctionTypes.DIVISION

        # if the incoming function contains subtraction in recursive definition
        elif re.match(SUBTRACTION_REGEX, func):
            app_logger.debug(f'Subtraction expression found in incoming function')
            self._parse_subtraction_expression(func)
            self.op = FunctionTypes.SUBTRACTION

        # if the incoming function is unsupported
        else:
            app_logger.info(f'The given function ({func}) is not supported.')

    def _parse_division_expression(self, func: str):
        '''
        Determine the a and d values given in this expression and parse them into their
        respective types. This function parse functions which match the form aT(n/d).
        '''
        match = re.search(r'\d?T\(n\/\d\)', func)
        if match:
            app_logger.debug(f'Printing match: {match.group()}')
            group_arr: List[str] = list(match.group())
            index: int = 0
            a_val: str = ''
            while group_arr[index] != 'T':
                a_val += group_arr[index]
                index += 1
            self.a = 1 if a_val == '' else int(a_val)
            while group_arr[index] != '/':
                index += 1
            b_val: str = ''.join(group_arr[index + 1: -1])
            self.b = Rational(b_val)

    def _parse_subtraction_expression(self, func: str):
        '''
        Determine the a and d values given in this expression and parse them into their
        respective types. This function parse functions which match the form aT(n-d).
        '''
        match = re.search(r'\d?T\(n-\d\)', func)
        if match:
            app_logger.debug(f'Printing match: {match.group()}')
            group_arr: List[str] = list(match.group())
            index: int = 0
            a_val: str = ''
            while group_arr[index] != 'T':
                a_val += group_arr[index]
                index += 1
            self.a = 1 if a_val == '' else int(a_val)
            while group_arr[index] != '-':
                index += 1
            b_val: str = ''.join(group_arr[index + 1: -1])
            self.b = Rational(b_val)


@dataclass(init=False)
class PolynomialFunction(Function):
    c: Union[str, Rational]
    d: Rational
    asymptotic_func: str = ''

    def __init__(self, func, c: Rational, d: Rational, asymptotic_func: str):
        super().__init__(func)
        self.c = c
        self.d = d
        self.asymptotic_func = asymptotic_func

    def __repr__(self):
        return f'T(n) = {self.a}T(n{self.op.value}{self.b}) + {self.asymptotic_func}({self.c}n^{self.d})'


def get_function(func: str) -> Function:
    '''
    Parse the cost function into its component pieces for the format
    cn^d. There can also be non-polynomial type function passed here,
    such as O(n) or O(n/3), we should also handle those functions.
    '''
    match = re.search(r'\+\s?(.*)', func)
    if match:
        func_match = match.groups()[0]
        if re.match(POLYNOMIAL_FUNCTION_REGEX, func_match):
            cost = func_match
            asymptotic_func = ''
            app_logger.debug(f'Printing function match: {func_match}')
        elif re.match(BIG_O_FUNCTION_REGEX, func_match):
            cost = 'c' + func_match[2: -1]
            asymptotic_func = func_match[:1]
            app_logger.debug(f'Parsed Big-O cost function: {cost}')
        elif re.match(THETA_FUNCTION_REGEX, func_match):
            cost = 'c' + func_match[6: -1]
            asymptotic_func = func_match[:5]
            app_logger.debug(f'Parsed Theta cost function: {cost}')
        elif re.match(OMEGA_FUNCTION_REGEX, func_match):
            cost = 'c' + func_match[6: -1]
            asymptotic_func = func_match[:5]
            app_logger.debug(f'Parsed Omega cost function: {cost}')
        elif re.match(CONSTANT_FUNCTION_REGEX, func_match):
            cost = func_match
            asymptotic_func = ''
            app_logger.debug(f'Printing constant function match: {func_match}')
        else:
            app_logger.debug(f'Couldn\'t parse given function {func}')
            return

        # parse c and d from cost function
        func_match_arr: List[str] = list(cost)
        index: int = 0
        c_val: str = ''
        while index < len(func_match_arr) and func_match_arr[index] != "n":
            c_val += func_match_arr[index]
            index += 1
        try:
            c_val = Rational(c_val)
        except:
            pass
        d_val = ''.join(func_match_arr[index + 2:])
        return PolynomialFunction(func, c_val, Rational(d_val), asymptotic_func)
