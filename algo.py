from tree import Node, Tree
from logger import init_logger
from function import PolynomialFunction

app_logger = init_logger()


def create_tree(func: PolynomialFunction, tree: Tree, layer: int = 4) -> Tree:
    # recursively compute until all 4 layers of the tree are printed
    if layer > 0:
        create_tree(func, tree, layer - 1)

    if layer == 0:
        return tree.append([Node.from_func(func, layer)], layer)
    elif layer < 4:
        num_leaves: int = func.a if func.a == 1 else func.a * layer
        return tree.append([Node.from_func(func, layer)] * num_leaves, layer)

    return tree
