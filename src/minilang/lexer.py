from __future__ import annotations

from .errors import LexerError
from .tokens import Token, TokenType


KEYWORDS = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.token_line = 1
        self.token_column = 1

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self.token_line = self.line
            self.token_column = self.column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def _scan_token(self) -> None:
        c = self._advance()

        single = {
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            "{": TokenType.LEFT_BRACE,
            "}": TokenType.RIGHT_BRACE,
            ";": TokenType.SEMICOLON,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
        }

        if c in single:
            self._add_token(single[c])
        elif c == "!":
            self._add_token(TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG)
        elif c == "=":
            self._add_token(TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL)
        elif c == "<":
            self._add_token(TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS)
        elif c == ">":
            self._add_token(TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER)
        elif c == "/":
            if self._match("/"):
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif c in {" ", "\r", "\t", "\n"}:
            return
        elif c == '"':
            self._string()
        elif c.isdigit():
            self._number()
        elif c.isalpha() or c == "_":
            self._identifier()
        else:
            raise LexerError(
                f"Unexpected character {c!r} at line {self.token_line}, "
                f"column {self.token_column}."
            )

    def _identifier(self) -> None:
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        text = self.source[self.start:self.current]
        self._add_token(KEYWORDS.get(text, TokenType.IDENTIFIER))

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()

        text = self.source[self.start:self.current]
        literal = float(text) if "." in text else int(text)
        self._add_token(TokenType.NUMBER, literal)

    def _string(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            self._advance()

        if self._is_at_end():
            raise LexerError(
                f"Unterminated string at line {self.token_line}, "
                f"column {self.token_column}."
            )

        self._advance()
        value = self.source[self.start + 1:self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        if c == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return c

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self._advance()
        return True

    def _peek(self) -> str:
        return "\0" if self._is_at_end() else self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _add_token(self, token_type: TokenType, literal=None) -> None:
        self.tokens.append(
            Token(
                token_type,
                self.source[self.start:self.current],
                literal,
                self.token_line,
                self.token_column,
            )
        )

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)
