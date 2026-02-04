"""CLI tests"""

import pytest
from click.testing import CliRunner
from xmind_converter.cli import cli


def test_cli_info():
    """Test CLI info command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "XMind Converter" in result.output


def test_cli_help():
    """Test CLI help information"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "command line tool" in result.output


def test_cli_convert_help():
    """Test convert command help information"""
    runner = CliRunner()
    result = runner.invoke(cli, ["convert", "--help"])
    assert result.exit_code == 0
    assert "Convert between different formats" in result.output
