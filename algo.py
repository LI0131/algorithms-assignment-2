import sys

from tree import Node, Tree
from logger import init_logger
from function import PolynomialFunction, get_function

app_logger = init_logger()


def create_tree(func: PolynomialFunction, tree: Tree = Tree(), layer: int = 4) -> Tree:
    # recursively compute until all 4 layers of the tree are printed
    if layer > 0:
        create_tree(func, tree, layer - 1)

    if layer == 0:
        return tree.append([Node.from_func(func, layer)], layer)
    elif layer < 4:
        num_leaves: int = func.a if func.a == 1 else func.a ** layer
        return tree.append([Node.from_func(func, layer)] * num_leaves, layer)

    return tree


if __name__ == "__main__":
    if len(sys.argv) == 2:
        func = get_function(sys.argv[-1])
        if func is not None:
            app_logger.info(f'Creating Recursion Tree for {func}')
            tree = create_tree(func)
            app_logger.info(f'{tree}')
        else:
            app_logger.info(f'Could not parse function {sys.argv[-1]}')
    else:
        print('Usage: pipenv run generate <recursive function>')
