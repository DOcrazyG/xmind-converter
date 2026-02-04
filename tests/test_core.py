"""Test core functionality - Cross-format conversions"""

import os
import pytest
import tempfile
from xmind_converter.core import CoreConverter
from xmind_converter.exceptions import ParserError, FileFormatError


class TestCoreConverter:
    """Test CoreConverter for cross-format conversions"""

    @pytest.fixture
    def converter(self):
        """Create CoreConverter instance"""
        return CoreConverter()

    @pytest.fixture
    def xmind_file(self):
        """Get path to test XMind file"""
        return os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.xmind")

    @pytest.fixture
    def csv_file(self):
        """Get path to test CSV file"""
        return os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.csv")

    @pytest.fixture
    def md_file(self):
        """Get path to test Markdown file"""
        return os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.md")

    @pytest.fixture
    def json_file(self):
        """Get path to test JSON file"""
        return os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.json")

    @pytest.fixture
    def html_file(self):
        """Get path to test HTML file"""
        return os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.html")

    def test_converter_initialization(self, converter):
        """Test CoreConverter initialization"""
        assert converter is not None
        assert "csv" in converter.converters
        assert "md" in converter.converters
        assert "html" in converter.converters
        assert "json" in converter.converters
        assert "xmind" in converter.converters
        assert "csv" in converter.parsers
        assert "md" in converter.parsers
        assert "html" in converter.parsers
        assert "json" in converter.parsers
        assert "xmind" in converter.parsers

    def test_load_from_xmind(self, converter, xmind_file):
        """Test loading XMind file to MindMap"""
        mindmap = converter.load_from(xmind_file)
        assert mindmap is not None
        assert mindmap.name == "Sports"
        assert mindmap.root_node.title == "Sports"
        assert len(mindmap.root_node.children) == 4

    def test_load_from_csv(self, converter, csv_file):
        """Test loading CSV file to MindMap"""
        mindmap = converter.load_from(csv_file)
        assert mindmap is not None
        assert mindmap.name == "From CSV"
        assert mindmap.root_node.title == "Sports"

    def test_load_from_markdown(self, converter, md_file):
        """Test loading Markdown file to MindMap"""
        mindmap = converter.load_from(md_file)
        assert mindmap is not None
        assert mindmap.name == "From Markdown"
        assert mindmap.root_node.title == "Sports"

    def test_load_from_json(self, converter, json_file):
        """Test loading JSON file to MindMap"""
        mindmap = converter.load_from(json_file)
        assert mindmap is not None
        assert mindmap.name == "Sports"
        assert mindmap.root_node.title == "Sports"

    def test_load_from_html(self, converter, html_file):
        """Test loading HTML file to MindMap"""
        mindmap = converter.load_from(html_file)
        assert mindmap is not None
        assert mindmap.name == "Sports"
        assert mindmap.root_node.title == "Sports"

    def test_load_from_nonexistent_file(self, converter):
        """Test loading nonexistent file raises error"""
        with pytest.raises(ParserError):
            converter.load_from("nonexistent.xmind")

    def test_load_from_unsupported_format(self, converter):
        """Test loading unsupported format raises error"""
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
            temp_file = f.name

        try:
            with pytest.raises(FileFormatError):
                converter.load_from(temp_file)
        finally:
            os.unlink(temp_file)

    def test_convert_to_csv(self, converter, xmind_file):
        """Test converting MindMap to CSV"""
        mindmap = converter.load_from(xmind_file)

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert_to(mindmap, "csv", temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "Sports" in content
            assert "Ball Sports" in content
        finally:
            os.unlink(temp_file)

    def test_convert_to_markdown(self, converter, xmind_file):
        """Test converting MindMap to Markdown"""
        mindmap = converter.load_from(xmind_file)

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert_to(mindmap, "md", temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "# Sports" in content
            assert "## Ball Sports" in content
        finally:
            os.unlink(temp_file)

    def test_convert_to_html(self, converter, xmind_file):
        """Test converting MindMap to HTML"""
        mindmap = converter.load_from(xmind_file)

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert_to(mindmap, "html", temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "<!DOCTYPE html>" in content
            assert "Sports" in content
        finally:
            os.unlink(temp_file)

    def test_convert_to_json(self, converter, xmind_file):
        """Test converting MindMap to JSON"""
        mindmap = converter.load_from(xmind_file)

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert_to(mindmap, "json", temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert '"name": "Sports"' in content
        finally:
            os.unlink(temp_file)

    def test_convert_to_unsupported_format(self, converter, xmind_file):
        """Test converting to unsupported format raises error"""
        mindmap = converter.load_from(xmind_file)

        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
            temp_file = f.name

        try:
            with pytest.raises(FileFormatError):
                converter.convert_to(mindmap, "xyz", temp_file)
        finally:
            os.unlink(temp_file)

    def test_convert_xmind_to_csv(self, converter, xmind_file):
        """Test direct conversion from XMind to CSV"""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert(xmind_file, temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "Sports" in content
        finally:
            os.unlink(temp_file)

    def test_convert_xmind_to_markdown(self, converter, xmind_file):
        """Test direct conversion from XMind to Markdown"""
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert(xmind_file, temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "# Sports" in content
        finally:
            os.unlink(temp_file)

    def test_convert_xmind_to_html(self, converter, xmind_file):
        """Test direct conversion from XMind to HTML"""
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert(xmind_file, temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "<!DOCTYPE html>" in content
        finally:
            os.unlink(temp_file)

    def test_convert_xmind_to_json(self, converter, xmind_file):
        """Test direct conversion from XMind to JSON"""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert(xmind_file, temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert '"name": "Sports"' in content
        finally:
            os.unlink(temp_file)

    def test_convert_csv_to_markdown(self, converter, csv_file):
        """Test direct conversion from CSV to Markdown"""
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert(csv_file, temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "# Sports" in content
        finally:
            os.unlink(temp_file)

    def test_convert_markdown_to_csv(self, converter, md_file):
        """Test direct conversion from Markdown to CSV"""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert(md_file, temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "Sports" in content
        finally:
            os.unlink(temp_file)

    def test_convert_json_to_html(self, converter, json_file):
        """Test direct conversion from JSON to HTML"""
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert(json_file, temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)

            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "<!DOCTYPE html>" in content
        finally:
            os.unlink(temp_file)

    def test_convert_with_explicit_formats(self, converter, xmind_file):
        """Test conversion with explicit format specification"""
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert(xmind_file, temp_file, input_format="xmind", output_format="md")
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)
        finally:
            os.unlink(temp_file)

    def test_round_trip_xmind_csv_xmind(self, converter, xmind_file):
        """Test round-trip conversion: XMind -> CSV -> XMind"""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            csv_file = f.name

        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
            xmind_out = f.name

        try:
            mindmap1 = converter.load_from(xmind_file)
            converter.convert_to(mindmap1, "csv", csv_file)
            mindmap2 = converter.load_from(csv_file)
            converter.convert_to(mindmap2, "xmind", xmind_out)

            assert os.path.exists(xmind_out)
        finally:
            os.unlink(csv_file)
            os.unlink(xmind_out)

    def test_round_trip_xmind_md_xmind(self, converter, xmind_file):
        """Test round-trip conversion: XMind -> Markdown -> XMind"""
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            md_file = f.name

        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
            xmind_out = f.name

        try:
            mindmap1 = converter.load_from(xmind_file)
            converter.convert_to(mindmap1, "md", md_file)
            mindmap2 = converter.load_from(md_file)
            converter.convert_to(mindmap2, "xmind", xmind_out)

            assert os.path.exists(xmind_out)
        finally:
            os.unlink(md_file)
            os.unlink(xmind_out)

    def test_auto_detect_input_format(self, converter, xmind_file):
        """Test auto-detection of input format from file extension"""
        mindmap = converter.load_from(xmind_file)
        assert mindmap is not None
        assert mindmap.name == "Sports"

    def test_auto_detect_output_format(self, converter, xmind_file):
        """Test auto-detection of output format from file extension"""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            temp_file = f.name

        try:
            result = converter.convert(xmind_file, temp_file)
            assert "Conversion completed" in result
            assert os.path.exists(temp_file)
        finally:
            os.unlink(temp_file)
