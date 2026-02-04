"""命令行工具测试"""

import pytest
from click.testing import CliRunner
from xmind_converter.cli import cli


def test_cli_info():
    """测试命令行工具的info命令"""
    runner = CliRunner()
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "XMind Converter" in result.output


def test_cli_help():
    """测试命令行工具的帮助信息"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "command line tool" in result.output


def test_cli_convert_help():
    """测试转换命令的帮助信息"""
    runner = CliRunner()
    result = runner.invoke(cli, ["convert", "--help"])
    assert result.exit_code == 0
    assert "Convert between different formats" in result.output


def test_cli_reverse_help():
    """测试反向转换命令的帮助信息"""
    runner = CliRunner()
    result = runner.invoke(cli, ["reverse", "--help"])
    assert result.exit_code == 0
    assert "Convert from other formats" in result.output
