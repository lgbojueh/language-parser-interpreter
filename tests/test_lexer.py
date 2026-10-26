import pytest

from minilang.errors import LexerError
from minilang.lexer import Lexer
from minilang.tokens import TokenType


def test_lexer_recognizes_keywords_identifiers_and_literals():
    tokens = Lexer('let answer = 42; print "ok";').scan_tokens()
    types = [token.type for token in tokens]

    assert types == [
        TokenType.LET,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.NUMBER,
        TokenType.SEMICOLON,
        TokenType.PRINT,
        TokenType.STRING,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]
    assert tokens[3].literal == 42
    assert tokens[6].literal == "ok"


def test_lexer_ignores_comments():
    tokens = Lexer("// comment\nlet x = 1;").scan_tokens()
    assert tokens[0].type == TokenType.LET


def test_lexer_reports_invalid_character_location():
    with pytest.raises(LexerError, match="line 1, column 1"):
        Lexer("@").scan_tokens()
