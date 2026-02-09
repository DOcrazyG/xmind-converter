"""Test converters - MindMap to various formats"""

import os
import pytest
import tempfile
import zipfile
import json
from xmind_converter.parsers.xmind_parser import XMindParser
from xmind_converter.converters.csv_converter import CSVConverter
from xmind_converter.converters.md_converter import MarkdownConverter
from xmind_converter.converters.html_converter import HTMLConverter
from xmind_converter.converters.json_converter import JSONConverter
from xmind_converter.converters.xmind_converter import XMindConverter


@pytest.fixture
def parser():
    """Create parser instance"""
    return XMindParser()


@pytest.fixture
def sports_mindmap(parser):
    """Load example_v8.xmind for testing"""
    xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "example_v8.xmind")
    return parser.parse(xmind_file)


class TestCSVConverter:
    """Test CSV converter functionality"""

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
            assert "Sports,Running,contains" in csv_content
            assert "Running,Marathon,contains" in csv_content
            assert "Sports,Swimming,contains" in csv_content
            assert "Swimming,Freestyle,contains" in csv_content
            assert "Sports,Basketball,contains" in csv_content
            assert "Basketball,NBA,contains" in csv_content
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


class TestMarkdownConverter:
    """Test Markdown converter functionality"""

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
            assert "- notes: This is a mind map about various sports" in md_content
            assert "- labels: [Healthy Living]" in md_content
            assert "## Running" in md_content
            assert "- notes: A type of aerobic exercise" in md_content
            assert "- labels: [Aerobic]" in md_content
            assert "### Marathon" in md_content
            assert "- notes: Long-distance running race" in md_content
            assert "- labels: [Challenge]" in md_content
            assert "## Swimming" in md_content
            assert "- notes: Full-body exercise" in md_content
            assert "- labels: [Full-body]" in md_content
            assert "## Basketball" in md_content
            assert "- notes: Team sport" in md_content
            assert "- labels: [Team]" in md_content
            assert "### NBA" in md_content
            assert "- notes: American professional basketball league" in md_content
            assert "- labels: [Professional]" in md_content
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


class TestHTMLConverter:
    """Test HTML converter functionality"""

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
            assert "<title>Sports Theme</title>" in html_content
            assert "Sports" in html_content
            assert "Running" in html_content
            assert "Marathon" in html_content
            assert "Swimming" in html_content
            assert "Freestyle" in html_content
            assert "Basketball" in html_content
            assert "NBA" in html_content
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


class TestJSONConverter:
    """Test JSON converter functionality"""

    def test_json_conversion(self, sports_mindmap):
        """Test JSON conversion from MindMap"""
        converter = JSONConverter()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8") as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)
            with open(temp_file, "r", encoding="utf-8") as f:
                json_content = f.read()

            assert '"title": "Sports Theme"' in json_content
            assert '"title": "Sports"' in json_content
            assert '"title": "Running"' in json_content
            assert '"title": "Marathon"' in json_content
            assert '"title": "Swimming"' in json_content
            assert '"title": "Freestyle"' in json_content
            assert '"title": "Basketball"' in json_content
            assert '"title": "NBA"' in json_content
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


class TestXMindConverter:
    """Test XMind converter functionality"""

    def test_xmind_conversion(self, sports_mindmap):
        """Test XMind conversion from MindMap"""
        converter = XMindConverter()
        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)

            assert os.path.exists(temp_file)
            assert zipfile.is_zipfile(temp_file)

            with zipfile.ZipFile(temp_file, "r") as zf:
                assert "content.json" in zf.namelist()
                assert "metadata.json" in zf.namelist()
                assert "manifest.json" in zf.namelist()
                assert "Thumbnails/thumbnail.png" in zf.namelist()

                content_json = json.loads(zf.read("content.json").decode("utf-8"))
                assert len(content_json) > 0
                assert content_json[0]["title"] == "Sports Theme"
                assert "rootTopic" in content_json[0]
                assert content_json[0]["rootTopic"]["title"] == "Sports"

                metadata_json = json.loads(zf.read("metadata.json").decode("utf-8"))
                assert "dataStructureVersion" in metadata_json
                assert "creator" in metadata_json

                manifest_json = json.loads(zf.read("manifest.json").decode("utf-8"))
                assert "file-entries" in manifest_json
        finally:
            os.unlink(temp_file)

    def test_xmind_conversion_round_trip(self, sports_mindmap):
        """Test XMind round-trip conversion (parse -> convert -> parse)"""
        converter = XMindConverter()
        parser = XMindParser()
        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)

            parsed_mindmap = parser.parse(temp_file)

            assert parsed_mindmap.title == sports_mindmap.title
            assert parsed_mindmap.topic_node.title == sports_mindmap.topic_node.title

            def compare_nodes(node1, node2):
                assert node1.title == node2.title
                if node1.notes:
                    assert node1.notes == node2.notes
                if node1.labels:
                    assert node1.labels == node2.labels
                assert len(node1.children) == len(node2.children)
                for child1, child2 in zip(node1.children, node2.children):
                    compare_nodes(child1, child2)

            compare_nodes(sports_mindmap.topic_node, parsed_mindmap.topic_node)
        finally:
            os.unlink(temp_file)

    def test_xmind_conversion_with_notes_and_labels(self, sports_mindmap):
        """Test XMind conversion preserves notes and labels"""
        converter = XMindConverter()
        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
            temp_file = f.name

        try:
            converter.convert_to(sports_mindmap, temp_file)

            with zipfile.ZipFile(temp_file, "r") as zf:
                content_json = json.loads(zf.read("content.json").decode("utf-8"))
                root_topic = content_json[0]["rootTopic"]

                assert "notes" in root_topic
                assert root_topic["notes"]["plain"]["content"] == "This is a mind map about various sports"

                assert "labels" in root_topic
                assert root_topic["labels"] == ["Healthy Living"]

                running_topic = root_topic["children"]["attached"][0]
                assert "notes" in running_topic
                assert running_topic["notes"]["plain"]["content"] == "A type of aerobic exercise"
                assert "labels" in running_topic
                assert running_topic["labels"] == ["Aerobic"]
        finally:
            os.unlink(temp_file)

    def test_xmind_conversion_with_detached_nodes(self, parser):
        """Test XMind conversion with detached nodes"""
        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "example_v8.xmind")
        mindmap = parser.parse(xmind_file)

        converter = XMindConverter()
        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
            temp_file = f.name

        try:
            converter.convert_to(mindmap, temp_file)

            with zipfile.ZipFile(temp_file, "r") as zf:
                content_json = json.loads(zf.read("content.json").decode("utf-8"))

                if "detachedTopics" in content_json[0]:
                    assert len(content_json[0]["detachedTopics"]) == len(mindmap.detached_nodes)
        finally:
            os.unlink(temp_file)

    def test_xmind_conversion_with_relations(self, parser):
        """Test XMind conversion with relations"""
        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "example_v8.xmind")
        mindmap = parser.parse(xmind_file)

        converter = XMindConverter()
        with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
            temp_file = f.name

        try:
            converter.convert_to(mindmap, temp_file)

            with zipfile.ZipFile(temp_file, "r") as zf:
                content_json = json.loads(zf.read("content.json").decode("utf-8"))

                if "relationships" in content_json[0]:
                    assert len(content_json[0]["relationships"]) == len(mindmap.relations)
                    for i, rel in enumerate(mindmap.relations):
                        assert content_json[0]["relationships"][i]["end1Id"] == rel.source_id
                        assert content_json[0]["relationships"][i]["end2Id"] == rel.target_id
                        assert content_json[0]["relationships"][i]["title"] == rel.title
        finally:
            os.unlink(temp_file)
