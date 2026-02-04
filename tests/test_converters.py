"""Test converters"""

import os
import pytest
from xmind_converter.parsers.xmind_parser import XMindParser
from xmind_converter.converters.csv_converter import CSVConverter
from xmind_converter.converters.md_converter import MarkdownConverter
from xmind_converter.converters.html_converter import HTMLConverter
from xmind_converter.converters.json_converter import JSONConverter


class TestConverters:
    """Test converter functionality"""

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
        """Test CSV conversion"""
        converter = CSVConverter()
        csv_content = converter.convert_to(sports_mindmap)

        assert "parent,child,relationship" in csv_content
        assert "Sports,Ball Sports,contains" in csv_content
        assert "Ball Sports,Basketball,contains" in csv_content
        assert "Water Sports,Swimming,contains" in csv_content
        assert "Individual Sports,Running,contains" in csv_content
        assert "Combat Sports,Boxing,contains" in csv_content

    def test_csv_conversion_from_file(self, sports_mindmap):
        """Test CSV conversion matches expected file"""
        converter = CSVConverter()
        csv_content = converter.convert_to(sports_mindmap)

        csv_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.csv")
        with open(csv_file, "r", encoding="utf-8") as f:
            expected_content = f.read()

        assert csv_content == expected_content

    def test_csv_reverse_conversion(self):
        """Test CSV reverse conversion"""
        converter = CSVConverter()
        csv_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.csv")
        mindmap = converter.convert_from(csv_file)

        assert mindmap.name == "From CSV"
        assert mindmap.root_node.title == "Sports"
        assert len(mindmap.root_node.children) == 4

        ball_sports = mindmap.root_node.children[0]
        assert ball_sports.title == "Ball Sports"
        assert len(ball_sports.children) == 3
        assert ball_sports.children[0].title == "Basketball"
        assert ball_sports.children[1].title == "Soccer"
        assert ball_sports.children[2].title == "Tennis"

    def test_md_conversion(self, sports_mindmap):
        """Test Markdown conversion"""
        converter = MarkdownConverter()
        md_content = converter.convert_to(sports_mindmap)

        assert "# Sports" in md_content
        assert "## Ball Sports" in md_content
        assert "### Basketball" in md_content
        assert "## Water Sports" in md_content
        assert "### Swimming" in md_content
        assert "## Individual Sports" in md_content
        assert "### Running" in md_content
        assert "## Combat Sports" in md_content
        assert "### Boxing" in md_content

    def test_md_conversion_from_file(self, sports_mindmap):
        """Test Markdown conversion matches expected file"""
        converter = MarkdownConverter()
        md_content = converter.convert_to(sports_mindmap)

        md_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.md")
        with open(md_file, "r", encoding="utf-8") as f:
            expected_content = f.read()

        assert md_content == expected_content

    def test_md_reverse_conversion(self):
        """Test Markdown reverse conversion"""
        converter = MarkdownConverter()
        md_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.md")
        mindmap = converter.convert_from(md_file)

        assert mindmap.name == "From Markdown"
        assert mindmap.root_node.title == "Sports"
        assert len(mindmap.root_node.children) == 4

        ball_sports = mindmap.root_node.children[0]
        assert ball_sports.title == "Ball Sports"
        assert len(ball_sports.children) == 3

    def test_html_conversion(self, sports_mindmap):
        """Test HTML conversion"""
        converter = HTMLConverter()
        html_content = converter.convert_to(sports_mindmap)

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

    def test_html_conversion_from_file(self, sports_mindmap):
        """Test HTML conversion matches expected file"""
        converter = HTMLConverter()
        html_content = converter.convert_to(sports_mindmap)

        html_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.html")
        with open(html_file, "r", encoding="utf-8") as f:
            expected_content = f.read()

        assert html_content == expected_content

    def test_json_conversion(self, sports_mindmap):
        """Test JSON conversion"""
        converter = JSONConverter()
        json_content = converter.convert_to(sports_mindmap)

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

    def test_json_conversion_from_file(self, sports_mindmap):
        """Test JSON conversion matches expected file"""
        converter = JSONConverter()
        json_content = converter.convert_to(sports_mindmap)

        json_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.json")
        with open(json_file, "r", encoding="utf-8") as f:
            expected_content = f.read()

        assert json_content == expected_content

    def test_round_trip_csv(self, sports_mindmap):
        """Test round-trip conversion: XMind -> CSV -> XMind"""
        csv_converter = CSVConverter()

        # Convert to CSV
        csv_content = csv_converter.convert_to(sports_mindmap)

        # Write to temp file
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", encoding="utf-8") as f:
            f.write(csv_content)
            temp_file = f.name

        try:
            # Convert back from CSV
            mindmap_from_csv = csv_converter.convert_from(temp_file)

            # Verify structure is preserved
            assert mindmap_from_csv.root_node.title == sports_mindmap.root_node.title
            assert len(mindmap_from_csv.root_node.children) == len(sports_mindmap.root_node.children)

            for i, child in enumerate(mindmap_from_csv.root_node.children):
                assert child.title == sports_mindmap.root_node.children[i].title
                assert len(child.children) == len(sports_mindmap.root_node.children[i].children)
        finally:
            os.unlink(temp_file)

    def test_round_trip_md(self, sports_mindmap):
        """Test round-trip conversion: XMind -> Markdown -> XMind"""
        md_converter = MarkdownConverter()

        # Convert to Markdown
        md_content = md_converter.convert_to(sports_mindmap)

        # Write to temp file
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
            f.write(md_content)
            temp_file = f.name

        try:
            # Convert back from Markdown
            mindmap_from_md = md_converter.convert_from(temp_file)

            # Verify structure is preserved
            assert mindmap_from_md.root_node.title == sports_mindmap.root_node.title
            assert len(mindmap_from_md.root_node.children) == len(sports_mindmap.root_node.children)

            for i, child in enumerate(mindmap_from_md.root_node.children):
                assert child.title == sports_mindmap.root_node.children[i].title
                assert len(child.children) == len(sports_mindmap.root_node.children[i].children)
        finally:
            os.unlink(temp_file)
