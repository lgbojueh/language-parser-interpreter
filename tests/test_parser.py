import pytest

from minilang.ast_nodes import IfStatement, LetStatement, PrintStatement, WhileStatement
from minilang.errors import ParserError
from minilang.lexer import Lexer
from minilang.parser import Parser


def parse(source: str):
    return Parser(Lexer(source).scan_tokens()).parse()


def test_parser_builds_expected_statement_types():
    program = parse(
        '''
        let x = 3;
        print x;
        if (x > 1) { print "yes"; } else { print "no"; }
        while (x > 0) { x = x - 1; }
        '''
    )

    assert isinstance(program.statements[0], LetStatement)
    assert isinstance(program.statements[1], PrintStatement)
    assert isinstance(program.statements[2], IfStatement)
    assert isinstance(program.statements[3], WhileStatement)


def test_parser_requires_semicolon():
    with pytest.raises(ParserError, match="Expected ';'"):
        parse("let x = 1")
