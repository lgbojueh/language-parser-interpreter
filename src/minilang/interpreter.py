from __future__ import annotations

from typing import Any, Callable

from .ast_nodes import (
    Assignment,
    Binary,
    Block,
    Grouping,
    IfStatement,
    LetStatement,
    Literal,
    PrintStatement,
    Program,
    Unary,
    Variable,
    WhileStatement,
)
from .errors import RuntimeExecutionError
from .tokens import TokenType


class Interpreter:
    def __init__(
        self,
        output: Callable[[str], None] = print,
        max_loop_iterations: int = 10_000,
    ):
        self.environment: dict[str, Any] = {}
        self.output = output
        self.max_loop_iterations = max_loop_iterations

    def execute(self, program: Program) -> dict[str, Any]:
        for statement in program.statements:
            self._execute_statement(statement)
        return dict(self.environment)

    def _execute_statement(self, statement):
        if isinstance(statement, LetStatement):
            name = statement.name.lexeme
            if name in self.environment:
                raise RuntimeExecutionError(f"Variable '{name}' is already defined.")
            self.environment[name] = self._evaluate(statement.initializer)
            return

        if isinstance(statement, Assignment):
            name = statement.name.lexeme
            if name not in self.environment:
                raise RuntimeExecutionError(f"Undefined variable '{name}'.")
            self.environment[name] = self._evaluate(statement.value)
            return

        if isinstance(statement, PrintStatement):
            self.output(self._stringify(self._evaluate(statement.expression)))
            return

        if isinstance(statement, Block):
            for nested in statement.statements:
                self._execute_statement(nested)
            return

        if isinstance(statement, IfStatement):
            if self._is_truthy(self._evaluate(statement.condition)):
                self._execute_statement(statement.then_branch)
            elif statement.else_branch is not None:
                self._execute_statement(statement.else_branch)
            return

        if isinstance(statement, WhileStatement):
            iterations = 0
            while self._is_truthy(self._evaluate(statement.condition)):
                iterations += 1
                if iterations > self.max_loop_iterations:
                    raise RuntimeExecutionError(
                        f"Loop exceeded the safety limit of "
                        f"{self.max_loop_iterations} iterations."
                    )
                self._execute_statement(statement.body)
            return

        raise RuntimeExecutionError(
            f"Unsupported statement type: {type(statement).__name__}"
        )

    def _evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, Variable):
            name = expression.name.lexeme
            if name not in self.environment:
                raise RuntimeExecutionError(f"Undefined variable '{name}'.")
            return self.environment[name]

        if isinstance(expression, Grouping):
            return self._evaluate(expression.expression)

        if isinstance(expression, Unary):
            right = self._evaluate(expression.right)
            if expression.operator.type == TokenType.BANG:
                return not self._is_truthy(right)
            if expression.operator.type == TokenType.MINUS:
                self._require_number(right, expression.operator.lexeme)
                return -right

        if isinstance(expression, Binary):
            left = self._evaluate(expression.left)
            right = self._evaluate(expression.right)
            token_type = expression.operator.type
            operator = expression.operator.lexeme

            if token_type == TokenType.PLUS:
                if self._is_number(left) and self._is_number(right):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                raise RuntimeExecutionError(
                    "Operator '+' requires two numbers or two strings."
                )

            if token_type in {
                TokenType.MINUS,
                TokenType.STAR,
                TokenType.SLASH,
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            }:
                self._require_number(left, operator)
                self._require_number(right, operator)

            if token_type == TokenType.MINUS:
                return left - right
            if token_type == TokenType.STAR:
                return left * right
            if token_type == TokenType.SLASH:
                if right == 0:
                    raise RuntimeExecutionError("Division by zero.")
                return left / right
            if token_type == TokenType.GREATER:
                return left > right
            if token_type == TokenType.GREATER_EQUAL:
                return left >= right
            if token_type == TokenType.LESS:
                return left < right
            if token_type == TokenType.LESS_EQUAL:
                return left <= right
            if token_type == TokenType.EQUAL_EQUAL:
                return left == right
            if token_type == TokenType.BANG_EQUAL:
                return left != right

        raise RuntimeExecutionError(
            f"Unsupported expression type: {type(expression).__name__}"
        )

    @staticmethod
    def _is_truthy(value: Any) -> bool:
        if value is False or value is None:
            return False
        if isinstance(value, (int, float)) and not isinstance(value, bool) and value == 0:
            return False
        if isinstance(value, str) and value == "":
            return False
        return True

    @staticmethod
    def _is_number(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def _require_number(self, value: Any, operator: str) -> None:
        if not self._is_number(value):
            raise RuntimeExecutionError(
                f"Operator '{operator}' requires numeric operands."
            )

    @staticmethod
    def _stringify(value: Any) -> str:
        if value is True:
            return "true"
        if value is False:
            return "false"
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)
