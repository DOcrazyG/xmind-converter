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

    def test_parse_sports_v8_xmind(self):
        """Test parsing sports_v8.xmind file (XMind 2024+ JSON format)"""
        parser = XMindParser()

        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.xmind")
        mindmap = parser.parse(xmind_file)

        assert mindmap is not None
        assert mindmap.name == "Sports"
        assert mindmap.root_node is not None
        assert mindmap.root_node.title == "Sports"

        assert len(mindmap.root_node.children) == 4

        child_titles = [child.title for child in mindmap.root_node.children]
        assert "Ball Sports" in child_titles
        assert "Water Sports" in child_titles
        assert "Individual Sports" in child_titles
        assert "Combat Sports" in child_titles

        ball_sports = next(child for child in mindmap.root_node.children if child.title == "Ball Sports")
        assert len(ball_sports.children) == 3
        ball_sports_titles = [child.title for child in ball_sports.children]
        assert "Basketball" in ball_sports_titles
        assert "Soccer" in ball_sports_titles
        assert "Tennis" in ball_sports_titles

        water_sports = next(child for child in mindmap.root_node.children if child.title == "Water Sports")
        assert len(water_sports.children) == 2
        water_sports_titles = [child.title for child in water_sports.children]
        assert "Swimming" in water_sports_titles
        assert "Boating" in water_sports_titles

        individual_sports = next(child for child in mindmap.root_node.children if child.title == "Individual Sports")
        assert len(individual_sports.children) == 2
        individual_sports_titles = [child.title for child in individual_sports.children]
        assert "Running" in individual_sports_titles
        assert "Gymnastics" in individual_sports_titles

        combat_sports = next(child for child in mindmap.root_node.children if child.title == "Combat Sports")
        assert len(combat_sports.children) == 2
        combat_sports_titles = [child.title for child in combat_sports.children]
        assert "Boxing" in combat_sports_titles
        assert "Judo" in combat_sports_titles

    def test_parse_sports_v75_xmind(self):
        """Test parsing sports_v75.xmind file (XMind 7.5 XML format)"""
        parser = XMindParser()

        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v75.xmind")
        mindmap = parser.parse(xmind_file)

        assert mindmap is not None
        assert mindmap.root_node is not None
        assert mindmap.root_node.title == "Sports"

        assert len(mindmap.root_node.children) == 4

        child_titles = [child.title for child in mindmap.root_node.children]
        assert "Ball Sports" in child_titles
        assert "Water Sports" in child_titles
        assert "Individual Sports" in child_titles
        assert "Combat Sports" in child_titles

        ball_sports = next(child for child in mindmap.root_node.children if child.title == "Ball Sports")
        assert len(ball_sports.children) == 3
        ball_sports_titles = [child.title for child in ball_sports.children]
        assert "Basketball" in ball_sports_titles
        assert "Soccer" in ball_sports_titles
        assert "Tennis" in ball_sports_titles

        water_sports = next(child for child in mindmap.root_node.children if child.title == "Water Sports")
        assert len(water_sports.children) == 2
        water_sports_titles = [child.title for child in water_sports.children]
        assert "Swimming" in water_sports_titles
        assert "Boating" in water_sports_titles

        individual_sports = next(child for child in mindmap.root_node.children if child.title == "Individual Sports")
        assert len(individual_sports.children) == 2
        individual_sports_titles = [child.title for child in individual_sports.children]
        assert "Running" in individual_sports_titles
        assert "Gymnastics" in individual_sports_titles

        combat_sports = next(child for child in mindmap.root_node.children if child.title == "Combat Sports")
        assert len(combat_sports.children) == 2
        combat_sports_titles = [child.title for child in combat_sports.children]
        assert "Boxing" in combat_sports_titles
        assert "Judo" in combat_sports_titles

    def test_parse_sports_v6_xmind(self):
        """Test parsing sports_v6.xmind file (XMind 6 XML format)"""
        parser = XMindParser()

        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v6.xmind")
        mindmap = parser.parse(xmind_file)

        assert mindmap is not None
        assert mindmap.root_node is not None
        assert mindmap.root_node.title == "Sports"

        assert len(mindmap.root_node.children) == 4

        child_titles = [child.title for child in mindmap.root_node.children]
        assert "Ball Sports" in child_titles
        assert "Water Sports" in child_titles
        assert "Individual Sports" in child_titles
        assert "Combat Sports" in child_titles

        ball_sports = next(child for child in mindmap.root_node.children if child.title == "Ball Sports")
        assert len(ball_sports.children) == 3
        ball_sports_titles = [child.title for child in ball_sports.children]
        assert "Basketball" in ball_sports_titles
        assert "Soccer" in ball_sports_titles
        assert "Tennis" in ball_sports_titles

        water_sports = next(child for child in mindmap.root_node.children if child.title == "Water Sports")
        assert len(water_sports.children) == 2
        water_sports_titles = [child.title for child in water_sports.children]
        assert "Swimming" in water_sports_titles
        assert "Boating" in water_sports_titles

        individual_sports = next(child for child in mindmap.root_node.children if child.title == "Individual Sports")
        assert len(individual_sports.children) == 2
        individual_sports_titles = [child.title for child in individual_sports.children]
        assert "Running" in individual_sports_titles
        assert "Gymnastics" in individual_sports_titles

        combat_sports = next(child for child in mindmap.root_node.children if child.title == "Combat Sports")
        assert len(combat_sports.children) == 2
        combat_sports_titles = [child.title for child in combat_sports.children]
        assert "Boxing" in combat_sports_titles
        assert "Judo" in combat_sports_titles


class TestCSVParser:
    """Test CSV parser - CSV format to MindMap"""

    def test_parse_csv_to_mindmap(self):
        """Test parsing CSV file to MindMap"""
        parser = CSVParser()
        csv_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.csv")
        mindmap = parser.parse(csv_file)

        assert mindmap.name == "From CSV"
        assert mindmap.root_node.title == "Sports"
        assert len(mindmap.root_node.children) == 4

        ball_sports = mindmap.root_node.children[0]
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

        assert mindmap.name == "From Markdown"
        assert mindmap.root_node.title == "Sports"
        assert len(mindmap.root_node.children) == 4

        ball_sports = mindmap.root_node.children[0]
        assert ball_sports.title == "Ball Sports"
        assert len(ball_sports.children) == 3


class TestJSONParser:
    """Test JSON parser - JSON format to MindMap"""

    def test_parse_json_to_mindmap(self):
        """Test parsing JSON file to MindMap"""
        parser = JSONParser()
        json_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.json")
        mindmap = parser.parse(json_file)

        assert mindmap.name == "Sports"
        assert mindmap.root_node.title == "Sports"
        assert len(mindmap.root_node.children) == 4

        ball_sports = mindmap.root_node.children[0]
        assert ball_sports.title == "Ball Sports"
        assert len(ball_sports.children) == 3


class TestHTMLParser:
    """Test HTML parser - HTML format to MindMap"""

    def test_parse_html_to_mindmap(self):
        """Test parsing HTML file to MindMap"""
        parser = HTMLParser()
        html_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.html")
        mindmap = parser.parse(html_file)

        assert mindmap.name == "Sports"
        assert mindmap.root_node.title == "Sports"
        assert len(mindmap.root_node.children) == 4
