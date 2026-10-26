import pytest

from minilang.errors import RuntimeExecutionError
from minilang.interpreter import Interpreter
from minilang.lexer import Lexer
from minilang.parser import Parser


def execute(source: str, max_loop_iterations=10_000):
    output = []
    program = Parser(Lexer(source).scan_tokens()).parse()
    interpreter = Interpreter(
        output=output.append,
        max_loop_iterations=max_loop_iterations,
    )
    environment = interpreter.execute(program)
    return output, environment


def test_arithmetic_precedence_and_assignment():
    output, environment = execute(
        '''
        let x = 2 + 3 * 4;
        x = x - 5;
        print x;
        '''
    )
    assert environment["x"] == 9
    assert output == ["9"]


def test_if_else_and_while():
    output, environment = execute(
        '''
        let x = 4;
        let total = 0;

        while (x > 0) {
            total = total + x;
            x = x - 1;
        }

        if (total == 10) {
            print "correct";
        } else {
            print "wrong";
        }
        '''
    )
    assert output == ["correct"]
    assert environment["total"] == 10
    assert environment["x"] == 0


def test_string_concatenation():
    output, _ = execute('print "hello " + "world";')
    assert output == ["hello world"]


def test_undefined_variable_is_runtime_error():
    with pytest.raises(RuntimeExecutionError, match="Undefined variable"):
        execute("print missing;")


def test_division_by_zero_is_runtime_error():
    with pytest.raises(RuntimeExecutionError, match="Division by zero"):
        execute("print 5 / 0;")


def test_loop_safety_limit():
    with pytest.raises(RuntimeExecutionError, match="safety limit"):
        execute("while (true) { print 1; }", max_loop_iterations=2)
