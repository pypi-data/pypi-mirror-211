"""testing csvsheet module."""

import io
from typing import Union

import pytest
from faker import Faker
from hypothesis import HealthCheck, example, given, settings, strategies as st
from pytest_mock import MockFixture

from csvsheet.csvsheet import main, run, sanitize_cell

__author__ = "Jesús Lázaro"
__copyright__ = "Jesús Lázaro"
__license__ = "MIT"


# create a fixture to test sanitize_cell
@pytest.mark.parametrize(
    ("cell", "expected"),
    [
        ("=1+1", 2),
        ("=1 + 1", 2),
        ("=1+1 # comment", 2),
        ("=1+1 # comment # comment", 2),
        ("=1+1 #", 2),
        ("=math.pi", 3.141592653589793),
        ("1+2", "1+2"),
        ("=int(1.0/2.0)", 0),
        ("=1+2", 3),
        pytest.param(
            '=import os; os.system("rm -rf /")',
            None,
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param("=1++", None, marks=pytest.mark.xfail(raises=SyntaxError)),
    ],
)
def test_sanitize_cell(
    cell: str,
    expected: Union[str, int, float],
):
    """Test sanitize_cell."""
    assert sanitize_cell(cell) == expected


# check different CSV delimiters
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,))
@given(delimiter=st.characters(whitelist_categories=("Zs", "P")))
def test_csv_delimeter(delimiter: str, mocker: MockFixture, capsys):
    """Test main with different CSV delimiters."""
    test_string = f"item{delimiter}a"
    mocker.patch("sys.stdin", io.StringIO(test_string))
    main(["-", "-o", "-", "-d", delimiter])
    # capture stdout
    captured = capsys.readouterr()
    assert captured.out == test_string + "\r\n"


# check mathdelimiter
@given(mathdelimiter=st.characters(blacklist_categories=("Cs", "Cc")))
@example("=")
def test_sanitize_cell_mathdelimiter(mathdelimiter: str):
    """Test sanitize_cell with mathdelimiter."""
    assert sanitize_cell(f"{mathdelimiter}1+1", mathdelimiter) == 2


# parametrize the main function
@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (
            ["tests/test_a.csv"],
            'item,a,b\r\nq,7,3+4\r\nw,21.0,0.75\r\nrtert,81.0,6\r\n"circle,area",18,m2\r\n',
        ),
        (
            ["tests/test_a.ssv", "-o", "-", "-d", ";", "-q", "'", "-m", "@"],
            "item;a;b\r\nq;7;3+4\r\nw;21.0;0.75\r\nrtert;81.0;6\r\ncircle,area;18;m2\r\n",
        ),
        pytest.param(
            ["input.csv", "-o", "-"],
            "argument INPUT_FILE: can't open 'input.csv'",
            marks=pytest.mark.xfail(raises=SystemExit),
        ),
        pytest.param(
            ["tests/test_b.csv", "-o", "-"],
            "Error: formula contains invalid characters",
            marks=pytest.mark.xfail(raises=SystemExit),
        ),
        pytest.param(
            ["tests/test_c.csv", "-o", "-"],
            "unexpected EOF while parsing",
            marks=pytest.mark.xfail(raises=SystemExit),
        ),
        pytest.param(
            ["-o", "-"],
            "error: the following arguments are required: INPUT_FILE",
            marks=pytest.mark.xfail(raises=SystemExit),
        ),
        pytest.param(
            [],
            "usage:",
            marks=pytest.mark.xfail(raises=SystemExit),
        ),
    ],
)
def test_main(capsys, args, expected):
    """CLI Tests, general examples."""
    main(args)
    captured = capsys.readouterr()
    assert captured.out == expected


# File creation test
def test_main_files(mocker: MockFixture, faker: Faker):
    """CLI Test file creation."""
    open = mocker.patch("builtins.open", mocker.mock_open(read_data="=1+1\n"))
    # run main
    for _i in range(100):
        input_file = faker.file_path()
        output_file = faker.file_path()
        main([input_file, "-o", output_file])

        # check file read
        open.assert_any_call(input_file, "r", -1, None, None)
        # check file write
        open.assert_called_with(output_file, "w", -1, None, None)
        # check write value: 2
        handle = open()
        handle.write.assert_any_call("2\r\n")


# Check stdin and stdout
def test_main_stdin_stdout(capsys, mocker: MockFixture):
    """CLI Test stdin and stdout."""
    test_string = "hello,world"
    mocker.patch("sys.stdin", io.StringIO(test_string))
    # run main
    main(["-", "-o", "-"])

    # capture stdout
    captured = capsys.readouterr()
    assert captured.out == test_string + "\r\n"


def test_simple_run():
    """Test run entry point."""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
