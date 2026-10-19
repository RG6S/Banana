"""AST node definitions for the Banana language (Part 4)."""

from dataclasses import dataclass
from typing import List


class Node:
    """Base class for all AST nodes."""

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
    operator: str
    operand: Node

    def label(self) -> str:
        return f"UnaryOpNode({self.operator})"

    def children(self) -> List[Node]:
        return [self.operand]


@dataclass(frozen=True)
class BinaryOpNode(Node):
    operator: str
    left: Node
    right: Node

    def label(self) -> str:
        return f"BinaryOpNode({self.operator})"

    def children(self) -> List[Node]:
        return [self.left, self.right]


@dataclass(frozen=True)
class AssignmentNode(Node):
    """Variable declaration, assignment, or compound assignment."""

    name: str
    operator: str
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
class IfNode(Node):
    """Conditional statement with then and optional else branches."""

    condition: Node
    then_branch: List[Node]
    else_branch: List[Node]

    def label(self) -> str:
        return "IfNode"

    def children(self) -> List[Node]:
        return [
            self.condition,
            ProgramNode(self.then_branch),
            ProgramNode(self.else_branch),
        ]


@dataclass(frozen=True)
class WhileNode(Node):
    """Loop that executes while its condition is true."""

    condition: Node
    body: List[Node]

    def label(self) -> str:
        return "WhileNode"

    def children(self) -> List[Node]:
        return [
            self.condition,
            ProgramNode(self.body),
        ]


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
            branch = "└── " if last else "├── "
            lines.append(prefix + branch + kid.label())

            next_prefix = prefix + ("    " if last else "│   ")
            walk(kid, next_prefix)

    walk(node, "")
    return "\n".join(lines)


def to_sexpr(node: Node) -> str:
    """Convert an AST node into a compact Lisp-style representation."""

    if isinstance(node, NumberNode):
        return str(node.value)

    if isinstance(node, VariableNode):
        return node.name

    if isinstance(node, UnaryOpNode):
        return f"(neg {to_sexpr(node.operand)})"

    if isinstance(node, BinaryOpNode):
        return (
            f"({node.operator} {to_sexpr(node.left)} "
            f"{to_sexpr(node.right)})"
        )

    if isinstance(node, AssignmentNode):
        head = (
            f"let{node.operator}"
            if node.is_declaration
            else node.operator
        )
        return f"({head} {node.name} {to_sexpr(node.value)})"

    if isinstance(node, PrintNode):
        return f"(print {to_sexpr(node.expression)})"

    if isinstance(node, IfNode):
        then_part = " ".join(to_sexpr(s) for s in node.then_branch)
        else_part = " ".join(to_sexpr(s) for s in node.else_branch)
        return (
            f"(if {to_sexpr(node.condition)} "
            f"(then {then_part}) (else {else_part}))"
        )

    if isinstance(node, WhileNode):
        body = " ".join(to_sexpr(s) for s in node.body)        
        return f"(while {to_sexpr(node.condition)} (body {body}))"

    if isinstance(node, ProgramNode):
        statements = " ".join(to_sexpr(s) for s in node.statements)
        return f"(program {statements})"

    raise TypeError(f"Unknown node type: {type(node).__name__}")
