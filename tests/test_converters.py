"""Test converters - MindMap to various formats"""

import os
import pytest
import tempfile
from xmind_converter.parsers.xmind_parser import XMindParser
from xmind_converter.converters.csv_converter import CSVConverter
from xmind_converter.converters.md_converter import MarkdownConverter
from xmind_converter.converters.html_converter import HTMLConverter
from xmind_converter.converters.json_converter import JSONConverter


class TestConverters:
    """Test converter functionality - MindMap to format conversions"""

    @pytest.fixture
    def parser(self):
        """Create parser instance"""
        return XMindParser()

    @pytest.fixture
    def sports_mindmap(self, parser):
        """Load sports_v8.xmind for testing"""
        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.xmind")
        return parser.parse(xmind_file)

    def test_csv_conversion(self, sports_mindmap):
        """Test CSV conversion from MindMap"""
        converter = CSVConverter()
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", encoding="utf-8") as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)
            with open(temp_file, "r", encoding="utf-8") as f:
                csv_content = f.read()

            assert "parent,child,relationship" in csv_content
            assert "Sports,Ball Sports,contains" in csv_content
            assert "Ball Sports,Basketball,contains" in csv_content
            assert "Water Sports,Swimming,contains" in csv_content
            assert "Individual Sports,Running,contains" in csv_content
            assert "Combat Sports,Boxing,contains" in csv_content
        finally:
            os.unlink(temp_file)

    def test_csv_conversion_from_file(self, sports_mindmap):
        """Test CSV conversion matches expected file"""
        converter = CSVConverter()
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", encoding="utf-8") as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)
            with open(temp_file, "r", encoding="utf-8") as f:
                csv_content = f.read()

            csv_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.csv")
            with open(csv_file, "r", encoding="utf-8") as f:
                expected_content = f.read()

            assert csv_content == expected_content
        finally:
            os.unlink(temp_file)

    def test_md_conversion(self, sports_mindmap):
        """Test Markdown conversion from MindMap"""
        converter = MarkdownConverter()
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)
            with open(temp_file, "r", encoding="utf-8") as f:
                md_content = f.read()

            assert "# Sports" in md_content
            assert "## Ball Sports" in md_content
            assert "### Basketball" in md_content
            assert "## Water Sports" in md_content
            assert "### Swimming" in md_content
            assert "## Individual Sports" in md_content
            assert "### Running" in md_content
            assert "## Combat Sports" in md_content
            assert "### Boxing" in md_content
        finally:
            os.unlink(temp_file)

    def test_md_conversion_from_file(self, sports_mindmap):
        """Test Markdown conversion matches expected file"""
        converter = MarkdownConverter()
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)
            with open(temp_file, "r", encoding="utf-8") as f:
                md_content = f.read()

            md_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.md")
            with open(md_file, "r", encoding="utf-8") as f:
                expected_content = f.read()

            assert md_content == expected_content
        finally:
            os.unlink(temp_file)

    def test_html_conversion(self, sports_mindmap):
        """Test HTML conversion from MindMap"""
        converter = HTMLConverter()
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)
            with open(temp_file, "r", encoding="utf-8") as f:
                html_content = f.read()

            assert "<!DOCTYPE html>" in html_content
            assert "<title>Sports</title>" in html_content
            assert "Sports" in html_content
            assert "Ball Sports" in html_content
            assert "Basketball" in html_content
            assert "Water Sports" in html_content
            assert "Swimming" in html_content
            assert "Individual Sports" in html_content
            assert "Running" in html_content
            assert "Combat Sports" in html_content
            assert "Boxing" in html_content
        finally:
            os.unlink(temp_file)

    def test_html_conversion_from_file(self, sports_mindmap):
        """Test HTML conversion matches expected file"""
        converter = HTMLConverter()
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)
            with open(temp_file, "r", encoding="utf-8") as f:
                html_content = f.read()

            html_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.html")
            with open(html_file, "r", encoding="utf-8") as f:
                expected_content = f.read()

            assert html_content == expected_content
        finally:
            os.unlink(temp_file)

    def test_json_conversion(self, sports_mindmap):
        """Test JSON conversion from MindMap"""
        converter = JSONConverter()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8") as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)
            with open(temp_file, "r", encoding="utf-8") as f:
                json_content = f.read()

            assert '"name": "Sports"' in json_content
            assert '"title": "Sports"' in json_content
            assert '"title": "Ball Sports"' in json_content
            assert '"title": "Basketball"' in json_content
            assert '"title": "Water Sports"' in json_content
            assert '"title": "Swimming"' in json_content
            assert '"title": "Individual Sports"' in json_content
            assert '"title": "Running"' in json_content
            assert '"title": "Combat Sports"' in json_content
            assert '"title": "Boxing"' in json_content
        finally:
            os.unlink(temp_file)

    def test_json_conversion_from_file(self, sports_mindmap):
        """Test JSON conversion matches expected file"""
        converter = JSONConverter()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8") as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)
            with open(temp_file, "r", encoding="utf-8") as f:
                json_content = f.read()

            json_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.json")
            with open(json_file, "r", encoding="utf-8") as f:
                expected_content = f.read()

            assert json_content == expected_content
        finally:
            os.unlink(temp_file)
