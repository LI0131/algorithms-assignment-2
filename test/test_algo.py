import logging

import algo
import settings

from tree import Tree
from function import get_function

app_logger = logging.getLogger(settings.APP_NAME)


def test_dnc_func_1():
    func = 'T(n) = 2T(n/2) + Theta(n)'
    app_logger.debug(f'Testing function: {func}')
    func = get_function(func)
    tree = algo.create_tree(func, Tree())
    app_logger.debug(f'Created Tree Result: {tree}')


def test_dnc_func_2():
    func = 'T(n) = 7T(n/2) + Theta(n^2)'
    app_logger.debug(f'Testing function: {func}')
    func = get_function(func)
    tree = algo.create_tree(func, Tree())
    app_logger.debug(f'Created Tree Result: {tree}')


def test_dnc_func_3():
    func = 'T(n) = 3T(n/4) + cn^2'
    app_logger.debug(f'Testing function: {func}')
    func = get_function(func)
    tree = algo.create_tree(func, Tree())
    app_logger.debug(f'Created Tree Result: {tree}')


def test_cnbc_func1():
    func = 'T(n) = T(n-1) + n'
    app_logger.debug(f'Testing function: {func}')
    func = get_function(func)
    tree = algo.create_tree(func, Tree())
    app_logger.debug(f'Created Tree Result: {tree}')


def test_cnbc_func2():
    func = 'T(n) = 2T(n-1) + 1'
    app_logger.debug(f'Testing function: {func}')
    func = get_function(func)
    tree = algo.create_tree(func, Tree())
    app_logger.debug(f'Created Tree Result: {tree}')


def test_cnbc_func3():
    func = 'T(n) = T(n-2) + n^2'
    app_logger.debug(f'Testing function: {func}')
    func = get_function(func)
    tree = algo.create_tree(func, Tree())
    app_logger.debug(f'Created Tree Result: {tree}')
