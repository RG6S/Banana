"""AST node definitions for the Banana language (Part 2)."""

from dataclasses import dataclass
from typing import List


class Node:
    """Base class. Every node can describe itself and list its children."""

    def label(self) -> str:
        raise NotImplementedError

    def children(self) -> List["Node"]:
        return []


@dataclass(frozen=True)
class NumberNode(Node):
    value: int

    def label(self) -> str:
        return f"NumberNode({self.value})"


@dataclass(frozen=True)
class VariableNode(Node):
    name: str

    def label(self) -> str:
        return f"VariableNode({self.name})"


@dataclass(frozen=True)
class UnaryOpNode(Node):
    operator: str          # currently only "-"
    operand: Node

    def label(self) -> str:
        return f"UnaryOpNode({self.operator})"

    def children(self) -> List[Node]:
        return [self.operand]


@dataclass(frozen=True)
class BinaryOpNode(Node):
    operator: str          # "+", "-", "*", "/"
    left: Node
    right: Node

    def label(self) -> str:
        return f"BinaryOpNode({self.operator})"

    def children(self) -> List[Node]:
        return [self.left, self.right]


@dataclass(frozen=True)
class AssignmentNode(Node):
    """`let x = e;` (is_declaration=True), `x = e;`, or `x += e;` etc.

    Compound operators are kept as written in `operator` ("+=", "-=", ...)
    rather than being rewritten into `x = x + e`. Desugaring can be done
    later (e.g. in an interpreter or code generator) if the group prefers.
    """
    name: str
    operator: str          # "=", "+=", "-=", "*=", "/="
    value: Node
    is_declaration: bool = False

    def label(self) -> str:
        prefix = "let " if self.is_declaration else ""
        return f"AssignmentNode({prefix}{self.name} {self.operator})"

    def children(self) -> List[Node]:
        return [self.value]


@dataclass(frozen=True)
class PrintNode(Node):
    expression: Node

    def label(self) -> str:
        return "PrintNode"

    def children(self) -> List[Node]:
        return [self.expression]


@dataclass(frozen=True)
class ProgramNode(Node):
    statements: List[Node]

    def label(self) -> str:
        return "ProgramNode"

    def children(self) -> List[Node]:
        return list(self.statements)


def format_tree(node: Node) -> str:
    """Pretty-print an AST as an indented tree."""
    lines = [node.label()]

    def walk(current: Node, prefix: str) -> None:
        kids = current.children()
        for index, kid in enumerate(kids):
            last = index == len(kids) - 1
            lines.append(prefix + ("└── " if last else "├── ") + kid.label())
            walk(kid, prefix + ("    " if last else "│   "))

    walk(node, "")
    return "\n".join(lines)


def to_sexpr(node: Node) -> str:
    """Compact Lisp-style form, handy for tests: 2 + 3 * 4 -> (+ 2 (* 3 4))."""
    if isinstance(node, NumberNode):
        return str(node.value)
    if isinstance(node, VariableNode):
        return node.name
    if isinstance(node, UnaryOpNode):
        return f"(neg {to_sexpr(node.operand)})"
    if isinstance(node, BinaryOpNode):
        return (f"({node.operator} {to_sexpr(node.left)} "
                f"{to_sexpr(node.right)})")
    if isinstance(node, AssignmentNode):
        head = f"let{node.operator}" if node.is_declaration else node.operator
        return f"({head} {node.name} {to_sexpr(node.value)})"
    if isinstance(node, PrintNode):
        return f"(print {to_sexpr(node.expression)})"
    if isinstance(node, ProgramNode):
        return "(program " + " ".join(to_sexpr(s) for s in node.statements) + ")"
    raise TypeError(f"Unknown node type: {type(node).__name__}")
