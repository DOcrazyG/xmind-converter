"""Command line tool"""

import click
import os
from .core import CoreConverter
from .exceptions import XMindConverterError


@click.group()
def cli():
    """XMind converter command line tool"""
    pass


@cli.command("convert")
@click.argument("input_file")
@click.argument("output_file")
@click.option("--input-format", "-i", help="Input format, supported: xmind, csv, md, html, json")
@click.option("--output-format", "-o", help="Output format, supported: xmind, csv, md, html, json")
def convert(input_file, output_file, input_format, output_format):
    """Convert between different formats"""
    try:
        converter = CoreConverter()
        result = converter.convert(input_file, output_file, input_format, output_format)
        click.echo(f"Conversion successful: {result}")
    except XMindConverterError as e:
        click.echo(f"Error: {str(e)}")
    except Exception as e:
        click.echo(f"Unknown error: {str(e)}")


@cli.command("info")
def info():
    """Show version information"""
    from . import __version__, __author__

    click.echo(f"XMind Converter v{__version__}")
    click.echo(f"Author: {__author__}")


if __name__ == "__main__":
    cli()
