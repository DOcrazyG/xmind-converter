"""Command line tool"""

import click
import os
from .core import XMindConverter
from .exceptions import XMindConverterError


@click.group()
def cli():
    """XMind converter command line tool"""
    pass


@cli.command("convert")
@click.argument("input_file")
@click.argument("output_file")
@click.option("--format", "-f", help="Output format, supported: csv, md, html, json")
def convert(input_file, output_file, format=None):
    """Convert XMind file to other formats"""
    # Auto detect output format
    if not format:
        ext = os.path.splitext(output_file)[1].lower()[1:]  # Remove dot
        if ext in ["csv", "md", "html", "json"]:
            format = ext
        else:
            click.echo("Error: Cannot auto detect output format, please specify with --format")
            return

    try:
        converter = XMindConverter()
        node = converter.load_xmind(input_file)
        result = converter.convert_to(node, format, output_file)
        click.echo(f"Conversion successful: {result}")
    except XMindConverterError as e:
        click.echo(f"Error: {str(e)}")
    except Exception as e:
        click.echo(f"Unknown error: {str(e)}")


@cli.command("reverse")
@click.argument("input_file")
@click.argument("output_file")
@click.option("--format", "-f", help="Input format, supported: csv, md, html, json")
def reverse(input_file, output_file, format=None):
    """Convert from other formats to XMind file"""
    # Auto detect input format
    if not format:
        ext = os.path.splitext(input_file)[1].lower()[1:]  # Remove dot
        if ext in ["csv", "md", "html", "json"]:
            format = ext
        else:
            click.echo("Error: Cannot auto detect input format, please specify with --format")
            return

    try:
        converter = XMindConverter()
        node = converter.convert_from(input_file, format)
        # Need to implement logic to save as XMind file here
        click.echo("Reverse conversion feature not fully implemented yet")
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
