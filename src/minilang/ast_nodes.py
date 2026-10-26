from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .tokens import Token


class Expr:
    pass


class Stmt:
    pass


@dataclass
class Literal(Expr):
    value: Any


@dataclass
class Variable(Expr):
    name: Token


@dataclass
class Grouping(Expr):
    expression: Expr


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class LetStatement(Stmt):
    name: Token
    initializer: Expr


@dataclass
class Assignment(Stmt):
    name: Token
    value: Expr


@dataclass
class PrintStatement(Stmt):
    expression: Expr


@dataclass
class Block(Stmt):
    statements: list[Stmt]


@dataclass
class IfStatement(Stmt):
    condition: Expr
    then_branch: Block
    else_branch: Block | None


@dataclass
class WhileStatement(Stmt):
    condition: Expr
    body: Block


@dataclass
class Program:
    statements: list[Stmt]
