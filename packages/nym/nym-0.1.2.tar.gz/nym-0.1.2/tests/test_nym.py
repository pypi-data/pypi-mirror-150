#!/usr/bin/env python

"""Tests for `nym` package."""

import pytest
from click.testing import CliRunner

from nym import cli, fast, slow


def test_python_fib():
    res = slow.fib(33)
    assert res == 3524578


def test_nim_fib():
    res = fast.fib(33)
    assert res == 3524578


@pytest.mark.parametrize("n", [0, 1, 5, 20])
def test_implementations_match(n):
    assert slow.fib(n) == fast.fib(n)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "nim fib implementation is" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
