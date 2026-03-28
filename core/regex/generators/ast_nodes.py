from dataclasses import dataclass


@dataclass
class Symbol:
    value: str

    def __repr__(self):
        return f"Symbol({self.value!r})"


@dataclass
class Union:
    left: object
    right: object

    def __repr__(self):
        return f"Union({self.left!r}, {self.right!r})"


@dataclass
class Concat:
    left: object
    right: object

    def __repr__(self):
        return f"Concat({self.left!r}, {self.right!r})"


@dataclass
class Star:
    inner: object

    def __repr__(self):
        return f"Star({self.inner!r})"


@dataclass
class Optional:
    inner: object

    def __repr__(self):
        return f"Optional({self.inner!r})"


def is_atomic(node) -> bool:
    return isinstance(node, Symbol)


def count_nodes(node) -> int:
    if isinstance(node, Symbol):
        return 1
    if isinstance(node, (Star, Optional)):
        return 1 + count_nodes(node.inner)
    if isinstance(node, (Union, Concat)):
        return 1 + count_nodes(node.left) + count_nodes(node.right)
    raise TypeError(f"Unknown node type: {type(node)}")


def count_unions(node) -> int:
    if isinstance(node, Union):
        return 1 + count_unions(node.left) + count_unions(node.right)
    if isinstance(node, Concat):
        return count_unions(node.left) + count_unions(node.right)
    if isinstance(node, (Star, Optional)):
        return count_unions(node.inner)
    if isinstance(node, Symbol):
        return 0
    raise TypeError(f"Unknown node type: {type(node)}")


def count_stars(node) -> int:
    if isinstance(node, Star):
        return 1 + count_stars(node.inner)
    if isinstance(node, Optional):
        return count_stars(node.inner)
    if isinstance(node, (Union, Concat)):
        return count_stars(node.left) + count_stars(node.right)
    if isinstance(node, Symbol):
        return 0
    raise TypeError(f"Unknown node type: {type(node)}")