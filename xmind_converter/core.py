"""Core parsing and data models"""

from .models import MindMap, MindNode
from .parsers.xmind_parser import XMindParser
from .converters.csv_converter import CSVConverter
from .converters.md_converter import MarkdownConverter
from .converters.html_converter import HTMLConverter
from .converters.json_converter import JSONConverter
from .exceptions import XMindConverterError


class XMindConverter:
    """XMind converter main class"""

    def __init__(self):
        self.parser = XMindParser()
        self.converters = {
            "csv": CSVConverter(),
            "md": MarkdownConverter(),
            "html": HTMLConverter(),
            "json": JSONConverter(),
        }

    def load_xmind(self, file_path):
        """Load XMind file"""
        try:
            return self.parser.parse(file_path)
        except Exception as e:
            raise XMindConverterError(f"Failed to load XMind file: {str(e)}")

    def convert_to(self, mindmap, format_type, output_path=None, **kwargs):
        """Convert to specified format"""
        if format_type not in self.converters:
            raise XMindConverterError(f"Unsupported format: {format_type}")

        converter = self.converters[format_type]
        try:
            result = converter.convert(mindmap, **kwargs)
            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result)
                return f"Conversion completed, output to: {output_path}"
            return result
        except Exception as e:
            raise XMindConverterError(f"Conversion failed: {str(e)}")

    def convert_from(self, input_path, format_type, output_path=None, **kwargs):
        """Convert from specified format"""
        if format_type not in self.converters:
            raise XMindConverterError(f"Unsupported format: {format_type}")

        converter = self.converters[format_type]
        try:
            mindmap = converter.convert_from(input_path, **kwargs)
            if output_path:
                # Need to implement logic to save as XMind file here
                pass
            return mindmap
        except Exception as e:
            raise XMindConverterError(f"Conversion failed: {str(e)}")
