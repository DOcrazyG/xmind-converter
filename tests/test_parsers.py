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

    def test_parse_example_v8_with_notes_and_labels(self):
        """Test parsing example_v8.xmind with notes and labels"""
        parser = XMindParser()

        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "example_v8.xmind")
        mindmap = parser.parse(xmind_file)

        assert mindmap.topic_node is not None
        assert mindmap.topic_node.notes == "This is a mind map about various sports"
        assert mindmap.topic_node.labels == ["Healthy Living"]

    def test_parse_example_v8_with_relations(self):
        """Test parsing example_v8.xmind with relations"""
        parser = XMindParser()

        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "example_v8.xmind")
        mindmap = parser.parse(xmind_file)

        assert len(mindmap.relations) == 2

        relation_titles = [rel.title for rel in mindmap.relations]
        assert "Aerobic Exercise" in relation_titles
        assert "Team Sport" in relation_titles


class TestCSVParser:
    """Test CSV parser - CSV format to MindMap"""

    def test_parse_csv_to_mindmap(self):
        """Test parsing CSV file to MindMap"""
        parser = CSVParser()
        csv_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.csv")
        mindmap = parser.parse(csv_file)

        assert mindmap.title == "From CSV"
        assert mindmap.topic_node.title == "Sports"
        assert len(mindmap.topic_node.children) == 3

        running = mindmap.topic_node.children[0]
        assert running.title == "Running"
        assert len(running.children) == 1
        assert running.children[0].title == "Marathon"

        swimming = mindmap.topic_node.children[1]
        assert swimming.title == "Swimming"
        assert len(swimming.children) == 1
        assert swimming.children[0].title == "Freestyle"

        basketball = mindmap.topic_node.children[2]
        assert basketball.title == "Basketball"
        assert len(basketball.children) == 1
        assert basketball.children[0].title == "NBA"

    def test_parse_csv_nonexistent_file(self):
        """Test parsing nonexistent CSV file"""
        from xmind_converter.exceptions import FileNotFound

        parser = CSVParser()
        with pytest.raises(FileNotFound):
            parser.parse("nonexistent.csv")

    def test_parse_csv_with_custom_delimiter(self):
        """Test parsing CSV file with custom delimiter"""
        parser = CSVParser()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write("parent;child;relationship\n")
            f.write("Root;Child1;contains\n")
            f.write("Child1;Grandchild;contains\n")
            temp_file = f.name

        try:
            mindmap = parser.parse(temp_file, delimiter=";")
            assert mindmap.topic_node.title == "Root"
            assert len(mindmap.topic_node.children) == 1
            assert mindmap.topic_node.children[0].title == "Child1"
            assert len(mindmap.topic_node.children[0].children) == 1
            assert mindmap.topic_node.children[0].children[0].title == "Grandchild"
        finally:
            os.unlink(temp_file)


class TestMarkdownParser:
    """Test Markdown parser - Markdown format to MindMap"""

    def test_parse_markdown_to_mindmap(self):
        """Test parsing Markdown file to MindMap"""
        parser = MarkdownParser()
        md_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.md")
        mindmap = parser.parse(md_file)

        assert mindmap.title == "From Markdown"
        assert mindmap.topic_node.title == "Sports"
        assert len(mindmap.topic_node.children) == 3

        running = mindmap.topic_node.children[0]
        assert running.title == "Running"
        assert len(running.children) == 1
        assert running.children[0].title == "Marathon"

        swimming = mindmap.topic_node.children[1]
        assert swimming.title == "Swimming"
        assert len(swimming.children) == 1
        assert swimming.children[0].title == "Freestyle"

        basketball = mindmap.topic_node.children[2]
        assert basketball.title == "Basketball"
        assert len(basketball.children) == 1
        assert basketball.children[0].title == "NBA"

    def test_parse_markdown_with_notes_and_labels(self):
        """Test parsing Markdown file with notes and labels"""
        parser = MarkdownParser()
        md_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.md")
        mindmap = parser.parse(md_file)

        assert mindmap.topic_node is not None
        assert mindmap.topic_node.notes == "This is a mind map about various sports"
        assert mindmap.topic_node.labels == ["Healthy Living"]

        running = mindmap.topic_node.children[0]
        assert running.notes == "A type of aerobic exercise"
        assert running.labels == ["Aerobic"]

        marathon = running.children[0]
        assert marathon.notes == "Long-distance running race"
        assert marathon.labels == ["Challenge"]

        swimming = mindmap.topic_node.children[1]
        assert swimming.notes == "Full-body exercise"
        assert swimming.labels == ["Full-body"]

        freestyle = swimming.children[0]
        assert freestyle.notes == "Most common swimming stroke"
        assert freestyle.labels == ["Basic"]

        basketball = mindmap.topic_node.children[2]
        assert basketball.notes == "Team sport"
        assert basketball.labels == ["Team"]

        nba = basketball.children[0]
        assert nba.notes == "American professional basketball league"
        assert nba.labels == ["Professional"]

    def test_parse_markdown_nonexistent_file(self):
        """Test parsing nonexistent Markdown file"""
        from xmind_converter.exceptions import FileNotFound

        parser = MarkdownParser()
        with pytest.raises(FileNotFound):
            parser.parse("nonexistent.md")


class TestJSONParser:
    """Test JSON parser - JSON format to MindMap"""

    def test_parse_json_to_mindmap(self):
        """Test parsing JSON file to MindMap"""
        parser = JSONParser()
        json_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.json")
        mindmap = parser.parse(json_file)

        assert mindmap.title == "Sports Theme"
        assert mindmap.topic_node.title == "Sports"
        assert len(mindmap.topic_node.children) == 3

        running = mindmap.topic_node.children[0]
        assert running.title == "Running"
        assert len(running.children) == 1
        assert running.children[0].title == "Marathon"

        swimming = mindmap.topic_node.children[1]
        assert swimming.title == "Swimming"
        assert len(swimming.children) == 1
        assert swimming.children[0].title == "Freestyle"

        basketball = mindmap.topic_node.children[2]
        assert basketball.title == "Basketball"
        assert len(basketball.children) == 1
        assert basketball.children[0].title == "NBA"

    def test_parse_json_with_notes_and_labels(self):
        """Test parsing JSON file with notes and labels"""
        parser = JSONParser()
        json_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.json")
        mindmap = parser.parse(json_file)

        assert mindmap.topic_node is not None
        assert mindmap.topic_node.notes == "This is a mind map about various sports"
        assert mindmap.topic_node.labels == ["Healthy Living"]

        running = mindmap.topic_node.children[0]
        assert running.notes == "A type of aerobic exercise"
        assert running.labels == ["Aerobic"]

        marathon = running.children[0]
        assert marathon.notes == "Long-distance running race"
        assert marathon.labels == ["Challenge"]

        swimming = mindmap.topic_node.children[1]
        assert swimming.notes == "Full-body exercise"
        assert swimming.labels == ["Full-body"]

        freestyle = swimming.children[0]
        assert freestyle.notes == "Most common swimming stroke"
        assert freestyle.labels == ["Basic"]

        basketball = mindmap.topic_node.children[2]
        assert basketball.notes == "Team sport"
        assert basketball.labels == ["Team"]

        nba = basketball.children[0]
        assert nba.notes == "American professional basketball league"
        assert nba.labels == ["Professional"]

    def test_parse_json_with_relations(self):
        """Test parsing JSON file with relations"""
        parser = JSONParser()
        json_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.json")
        mindmap = parser.parse(json_file)

        assert len(mindmap.relations) == 2

        relation_titles = [rel.title for rel in mindmap.relations]
        assert "Aerobic Exercise" in relation_titles
        assert "Team Sport" in relation_titles

    def test_parse_json_nonexistent_file(self):
        """Test parsing nonexistent JSON file"""
        from xmind_converter.exceptions import FileNotFound

        parser = JSONParser()
        with pytest.raises(FileNotFound):
            parser.parse("nonexistent.json")


class TestHTMLParser:
    """Test HTML parser - HTML format to MindMap"""

    def test_parse_html_to_mindmap(self):
        """Test parsing HTML file to MindMap"""
        parser = HTMLParser()
        html_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.html")
        mindmap = parser.parse(html_file)

        assert mindmap.title == "Sports Theme"
        assert mindmap.topic_node.title == "Sports"
        assert len(mindmap.topic_node.children) == 3

        running = mindmap.topic_node.children[0]
        assert running.title == "Running"
        assert len(running.children) == 1
        assert running.children[0].title == "Marathon"

        swimming = mindmap.topic_node.children[1]
        assert swimming.title == "Swimming"
        assert len(swimming.children) == 1
        assert swimming.children[0].title == "Freestyle"

        basketball = mindmap.topic_node.children[2]
        assert basketball.title == "Basketball"
        assert len(basketball.children) == 1
        assert basketball.children[0].title == "NBA"

    def test_parse_html_nonexistent_file(self):
        """Test parsing nonexistent HTML file"""
        from xmind_converter.exceptions import FileNotFound

        parser = HTMLParser()
        with pytest.raises(FileNotFound):
            parser.parse("nonexistent.html")

    def test_parse_html_with_title_tag(self):
        """Test parsing HTML file with title tag"""
        parser = HTMLParser()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("<title>Test MindMap</title>\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("<h1>Root</h1>\n")
            f.write("<h2>Child</h2>\n")
            f.write("</body>\n")
            f.write("</html>\n")
            temp_file = f.name

        try:
            mindmap = parser.parse(temp_file)
            assert mindmap.title == "Test MindMap"
            assert mindmap.topic_node.title == "Root"
            assert len(mindmap.topic_node.children) == 1
            assert mindmap.topic_node.children[0].title == "Child"
        finally:
            os.unlink(temp_file)
