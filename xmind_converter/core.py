"""Core parsing and data models"""

from typing import Dict, Optional
from .models import MindMap
from .parsers.xmind_parser import XMindParser
from .parsers.csv_parser import CSVParser
from .parsers.md_parser import MarkdownParser
from .parsers.html_parser import HTMLParser
from .parsers.json_parser import JSONParser
from .converters.csv_converter import CSVConverter
from .converters.md_converter import MarkdownConverter
from .converters.html_converter import HTMLConverter
from .converters.json_converter import JSONConverter
from .converters.xmind_converter import XMindConverter
from .exceptions import ParserError, ConverterError, FileFormatError


class CoreConverter:
    """XMind converter main class"""

    def __init__(self) -> None:
        self.converters: Dict[
            str, CSVConverter | MarkdownConverter | HTMLConverter | JSONConverter | XMindConverter
        ] = {
            "csv": CSVConverter(),
            "md": MarkdownConverter(),
            "html": HTMLConverter(),
            "json": JSONConverter(),
            "xmind": XMindConverter(),
        }
        self.parsers: Dict[str, XMindParser | CSVParser | MarkdownParser | HTMLParser | JSONParser] = {
            "xmind": XMindParser(),
            "csv": CSVParser(),
            "md": MarkdownParser(),
            "html": HTMLParser(),
            "json": JSONParser(),
        }

    def load_from(self, input_path: str, format_type: Optional[str] = None, **kwargs) -> MindMap:
        """Load from specified format and convert to MindMap

        Args:
            input_path: Path to input file
            format_type: Format type (auto-detected from file extension if not provided)
            **kwargs: Additional format-specific parameters

        Returns:
            MindMap object
        """
        if not format_type:
            import os

            ext = os.path.splitext(input_path)[1].lower()[1:]
            if ext in self.parsers:
                format_type = ext
            else:
                raise FileFormatError(f"Cannot auto detect format from file extension: {ext}")

        if format_type not in self.parsers:
            raise FileFormatError(f"Unsupported format: {format_type}")

        parser = self.parsers[format_type]
        try:
            return parser.parse(input_path, **kwargs)
        except Exception as e:
            raise ParserError(f"Failed to load file: {str(e)}")

    def convert_to(self, mindmap: MindMap, format_type: str, output_path: str, **kwargs) -> str:
        """Convert to specified format

        Args:
            mindmap: MindMap object to convert
            format_type: Target format type
            output_path: Path to save the output file
            **kwargs: Additional format-specific parameters

        Returns:
            Success message
        """
        if format_type not in self.converters:
            raise FileFormatError(f"Unsupported format: {format_type}")

        converter = self.converters[format_type]
        try:
            converter.convert_to(mindmap, output_path, **kwargs)
            return f"Conversion completed, output to: {output_path}"
        except Exception as e:
            raise ConverterError(f"Conversion failed: {str(e)}")

    def convert(
        self,
        input_path: str,
        output_path: str,
        input_format: Optional[str] = None,
        output_format: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Convert from one format to another

        Args:
            input_path: Path to input file
            output_path: Path to save the output file
            input_format: Input format type (auto-detected from file extension if not provided)
            output_format: Output format type (auto-detected from file extension if not provided)
            **kwargs: Additional format-specific parameters

        Returns:
            Success message
        """
        if not input_format:
            import os

            ext = os.path.splitext(input_path)[1].lower()[1:]
            if ext in self.parsers:
                input_format = ext
            else:
                raise FileFormatError(f"Cannot auto detect input format from file extension: {ext}")

        if not output_format:
            import os

            ext = os.path.splitext(output_path)[1].lower()[1:]
            if ext in self.converters:
                output_format = ext
            else:
                raise FileFormatError(f"Cannot auto detect output format from file extension: {ext}")

        mindmap = self.load_from(input_path, input_format, **kwargs)
        return self.convert_to(mindmap, output_format, output_path, **kwargs)
