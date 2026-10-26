from minilang.cli import run_source


def test_run_source_can_parse_without_execution(capsys):
    program = run_source("let x = 1;", no_run=True)
    assert len(program.statements) == 1
    assert capsys.readouterr().out == ""
