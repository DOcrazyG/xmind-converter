"""Test parsers - Various formats to MindMap"""

import pytest
import os
import tempfile
import zipfile
from xmind_converter.parsers.xmind_parser import XMindParser
from xmind_converter.parsers.csv_parser import CSVParser
from xmind_converter.parsers.md_parser import MarkdownParser
from xmind_converter.parsers.json_parser import JSONParser
from xmind_converter.parsers.html_parser import HTMLParser
from xmind_converter.exceptions import ParserError


class TestXMindParser:
    """Test XMind parser - XMind format to MindMap"""

    def test_parse_nonexistent_file(self):
        """Test parsing nonexistent file"""
        from xmind_converter.exceptions import FileNotFound

        parser = XMindParser()
        with pytest.raises(FileNotFound):
            parser.parse("nonexistent.xmind")

    def test_parse_invalid_file(self):
        """Test parsing invalid file"""
        from xmind_converter.exceptions import FileFormatError

        parser = XMindParser()
        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
            f.write(b"invalid content")
            temp_file = f.name

        try:
            with pytest.raises(FileFormatError):
                parser.parse(temp_file)
        finally:
            os.unlink(temp_file)

    def test_parse_empty_xmind(self):
        """Test parsing empty XMind file"""
        parser = XMindParser()
        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
            temp_file = f.name

        with zipfile.ZipFile(temp_file, "w") as zf:
            pass

        try:
            with pytest.raises(ParserError):
                parser.parse(temp_file)
        finally:
            os.unlink(temp_file)

    def test_parse_example_v8_xmind(self):
        """Test parsing example_v8.xmind file (XMind 2024+ JSON format)"""
        parser = XMindParser()

        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "example_v8.xmind")
        mindmap = parser.parse(xmind_file)

        assert mindmap is not None
        assert mindmap.title == "Sports Theme"
        assert mindmap.topic_node is not None
        assert mindmap.topic_node.title == "Sports"

        assert len(mindmap.topic_node.children) == 3

        child_titles = [child.title for child in mindmap.topic_node.children]
        assert "Running" in child_titles
        assert "Swimming" in child_titles
        assert "Basketball" in child_titles

        assert len(mindmap.relations) == 2

    def test_parse_example_v75_xmind(self):
        """Test parsing example_v7.5.xmind file (XMind 7.5 XML format)"""
        parser = XMindParser()

        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "example_v7.5.xmind")
        mindmap = parser.parse(xmind_file)

        assert mindmap is not None
        assert mindmap.title == "Untitled"
        assert mindmap.topic_node is not None
        assert mindmap.topic_node.title == "Sports"

        assert len(mindmap.topic_node.children) == 3

        child_titles = [child.title for child in mindmap.topic_node.children]
        assert "Running" in child_titles
        assert "Swimming" in child_titles
        assert "Basketball" in child_titles

        assert len(mindmap.relations) == 5

    def test_parse_example_v6_xmind(self):
        """Test parsing example_v6.xmind file (XMind 6 XML format)"""
        parser = XMindParser()

        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "example_v6.xmind")
        mindmap = parser.parse(xmind_file)

        assert mindmap is not None
        assert mindmap.title == "Untitled"
        assert mindmap.topic_node is not None
        assert mindmap.topic_node.title == "Sports"

        assert len(mindmap.topic_node.children) == 3

        child_titles = [child.title for child in mindmap.topic_node.children]
        assert "Running" in child_titles
        assert "Swimming" in child_titles
        assert "Basketball" in child_titles

        assert len(mindmap.relations) == 5


class TestCSVParser:
    """Test CSV parser - CSV format to MindMap"""

    def test_parse_csv_to_mindmap(self):
        """Test parsing CSV file to MindMap"""
        parser = CSVParser()
        csv_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.csv")
        mindmap = parser.parse(csv_file)

        assert mindmap.title == "From CSV"
        assert mindmap.topic_node.title == "Sports"
        assert len(mindmap.topic_node.children) == 4

        ball_sports = mindmap.topic_node.children[0]
        assert ball_sports.title == "Ball Sports"
        assert len(ball_sports.children) == 3
        assert ball_sports.children[0].title == "Basketball"
        assert ball_sports.children[1].title == "Soccer"
        assert ball_sports.children[2].title == "Tennis"


class TestMarkdownParser:
    """Test Markdown parser - Markdown format to MindMap"""

    def test_parse_markdown_to_mindmap(self):
        """Test parsing Markdown file to MindMap"""
        parser = MarkdownParser()
        md_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.md")
        mindmap = parser.parse(md_file)

        assert mindmap.title == "From Markdown"
        assert mindmap.topic_node.title == "Sports"
        assert len(mindmap.topic_node.children) == 4

        ball_sports = mindmap.topic_node.children[0]
        assert ball_sports.title == "Ball Sports"
        assert len(ball_sports.children) == 3


class TestJSONParser:
    """Test JSON parser - JSON format to MindMap"""

    def test_parse_json_to_mindmap(self):
        """Test parsing JSON file to MindMap"""
        parser = JSONParser()
        json_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.json")
        mindmap = parser.parse(json_file)

        assert mindmap.title == "Sports"
        assert mindmap.topic_node.title == "Sports"
        assert len(mindmap.topic_node.children) == 4

        ball_sports = mindmap.topic_node.children[0]
        assert ball_sports.title == "Ball Sports"
        assert len(ball_sports.children) == 3


class TestHTMLParser:
    """Test HTML parser - HTML format to MindMap"""

    def test_parse_html_to_mindmap(self):
        """Test parsing HTML file to MindMap"""
        parser = HTMLParser()
        html_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.html")
        mindmap = parser.parse(html_file)

        assert mindmap.title == "Sports"
        assert mindmap.topic_node.title == "Sports"
        assert len(mindmap.topic_node.children) == 4
