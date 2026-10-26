from __future__ import annotations

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
from .errors import ParserError
from .tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        statements = []
        while not self._is_at_end():
            statements.append(self._statement())
        return Program(statements)

    def _statement(self):
        if self._match(TokenType.LET):
            return self._let_statement()
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.LEFT_BRACE):
            return Block(self._block())

        if self._check(TokenType.IDENTIFIER) and self._check_next(TokenType.EQUAL):
            return self._assignment()

        raise self._error(self._peek(), "Expected a statement.")

    def _let_statement(self):
        name = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'let'.")
        self._consume(TokenType.EQUAL, "Expected '=' after variable name.")
        initializer = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration.")
        return LetStatement(name, initializer)

    def _assignment(self):
        name = self._advance()
        self._consume(TokenType.EQUAL, "Expected '=' after variable name.")
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after assignment.")
        return Assignment(name, value)

    def _print_statement(self):
        expression = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after print statement.")
        return PrintStatement(expression)

    def _if_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'if'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after if condition.")
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before if body.")
        then_branch = Block(self._block())

        else_branch = None
        if self._match(TokenType.ELSE):
            self._consume(TokenType.LEFT_BRACE, "Expected '{' before else body.")
            else_branch = Block(self._block())

        return IfStatement(condition, then_branch, else_branch)

    def _while_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'while'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after while condition.")
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before while body.")
        return WhileStatement(condition, Block(self._block()))

    def _block(self):
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            statements.append(self._statement())

        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after block.")
        return statements

    def _expression(self):
        return self._equality()

    def _equality(self):
        expression = self._comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            expression = Binary(expression, self._previous(), self._comparison())
        return expression

    def _comparison(self):
        expression = self._term()
        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            expression = Binary(expression, self._previous(), self._term())
        return expression

    def _term(self):
        expression = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            expression = Binary(expression, self._previous(), self._factor())
        return expression

    def _factor(self):
        expression = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            expression = Binary(expression, self._previous(), self._unary())
        return expression

    def _unary(self):
        if self._match(TokenType.BANG, TokenType.MINUS):
            return Unary(self._previous(), self._unary())
        return self._primary()

    def _primary(self):
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)
        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())
        if self._match(TokenType.LEFT_PAREN):
            expression = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return Grouping(expression)

        raise self._error(self._peek(), "Expected expression.")

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return token_type == TokenType.EOF
        return self._peek().type == token_type

    def _check_next(self, token_type: TokenType) -> bool:
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    @staticmethod
    def _error(token: Token, message: str) -> ParserError:
        location = "end of input" if token.type == TokenType.EOF else repr(token.lexeme)
        return ParserError(
            f"{message} Found {location} at line {token.line}, column {token.column}."
        )
