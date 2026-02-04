"""Parser tests"""

import pytest
import os
import tempfile
import zipfile
from xmind_converter.parsers.xmind_parser import XMindParser
from xmind_converter.exceptions import ParserError


def test_parse_nonexistent_file():
    """Test parsing nonexistent file"""
    parser = XMindParser()
    with pytest.raises(ParserError):
        parser.parse("nonexistent.xmind")


def test_parse_invalid_file():
    """Test parsing invalid file"""
    parser = XMindParser()
    # Create a non-zip file
    with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
        f.write(b"invalid content")
        temp_file = f.name

    try:
        with pytest.raises(ParserError):
            parser.parse(temp_file)
    finally:
        os.unlink(temp_file)


def test_parse_empty_xmind():
    """Test parsing empty XMind file"""
    parser = XMindParser()
    # Create an empty zip file
    with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
        temp_file = f.name

    with zipfile.ZipFile(temp_file, "w") as zf:
        pass

    try:
        with pytest.raises(ParserError):
            parser.parse(temp_file)
    finally:
        os.unlink(temp_file)


def test_parse_sports_v8_xmind():
    """Test parsing sports_v8.xmind file (XMind 2024+ JSON format)"""
    parser = XMindParser()

    xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.xmind")

    # Parse XMind file
    mindmap = parser.parse(xmind_file)

    # Verify parsing result
    assert mindmap is not None
    assert mindmap.name == "Sports"
    assert mindmap.root_node is not None
    assert mindmap.root_node.title == "Sports"

    # Verify there are 4 main categories
    assert len(mindmap.root_node.children) == 4

    # Verify child node titles
    child_titles = [child.title for child in mindmap.root_node.children]
    assert "Ball Sports" in child_titles
    assert "Water Sports" in child_titles
    assert "Individual Sports" in child_titles
    assert "Combat Sports" in child_titles

    # Verify Ball Sports child nodes
    ball_sports = next(child for child in mindmap.root_node.children if child.title == "Ball Sports")
    assert len(ball_sports.children) == 3
    ball_sports_titles = [child.title for child in ball_sports.children]
    assert "Basketball" in ball_sports_titles
    assert "Soccer" in ball_sports_titles
    assert "Tennis" in ball_sports_titles

    # Verify Water Sports child nodes
    water_sports = next(child for child in mindmap.root_node.children if child.title == "Water Sports")
    assert len(water_sports.children) == 2
    water_sports_titles = [child.title for child in water_sports.children]
    assert "Swimming" in water_sports_titles
    assert "Boating" in water_sports_titles

    # Verify Individual Sports child nodes
    individual_sports = next(child for child in mindmap.root_node.children if child.title == "Individual Sports")
    assert len(individual_sports.children) == 2
    individual_sports_titles = [child.title for child in individual_sports.children]
    assert "Running" in individual_sports_titles
    assert "Gymnastics" in individual_sports_titles

    # Verify Combat Sports child nodes
    combat_sports = next(child for child in mindmap.root_node.children if child.title == "Combat Sports")
    assert len(combat_sports.children) == 2
    combat_sports_titles = [child.title for child in combat_sports.children]
    assert "Boxing" in combat_sports_titles
    assert "Judo" in combat_sports_titles


def test_parse_sports_v75_xmind():
    """Test parsing sports_v75.xmind file (XMind 7.5 XML format)"""
    parser = XMindParser()

    xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v75.xmind")

    # Parse XMind file
    mindmap = parser.parse(xmind_file)

    # Verify parsing result
    assert mindmap is not None
    assert mindmap.root_node is not None
    assert mindmap.root_node.title == "Sports"

    # Verify there are 4 main categories
    assert len(mindmap.root_node.children) == 4

    # Verify child node titles
    child_titles = [child.title for child in mindmap.root_node.children]
    assert "Ball Sports" in child_titles
    assert "Water Sports" in child_titles
    assert "Individual Sports" in child_titles
    assert "Combat Sports" in child_titles

    # Verify Ball Sports child nodes
    ball_sports = next(child for child in mindmap.root_node.children if child.title == "Ball Sports")
    assert len(ball_sports.children) == 3
    ball_sports_titles = [child.title for child in ball_sports.children]
    assert "Basketball" in ball_sports_titles
    assert "Soccer" in ball_sports_titles
    assert "Tennis" in ball_sports_titles

    # Verify Water Sports child nodes
    water_sports = next(child for child in mindmap.root_node.children if child.title == "Water Sports")
    assert len(water_sports.children) == 2
    water_sports_titles = [child.title for child in water_sports.children]
    assert "Swimming" in water_sports_titles
    assert "Boating" in water_sports_titles

    # Verify Individual Sports child nodes
    individual_sports = next(child for child in mindmap.root_node.children if child.title == "Individual Sports")
    assert len(individual_sports.children) == 2
    individual_sports_titles = [child.title for child in individual_sports.children]
    assert "Running" in individual_sports_titles
    assert "Gymnastics" in individual_sports_titles

    # Verify Combat Sports child nodes
    combat_sports = next(child for child in mindmap.root_node.children if child.title == "Combat Sports")
    assert len(combat_sports.children) == 2
    combat_sports_titles = [child.title for child in combat_sports.children]
    assert "Boxing" in combat_sports_titles
    assert "Judo" in combat_sports_titles


def test_parse_sports_v6_xmind():
    """Test parsing sports_v6.xmind file (XMind 6 XML format)"""
    parser = XMindParser()

    xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v6.xmind")

    # Parse XMind file
    mindmap = parser.parse(xmind_file)

    # Verify parsing result
    assert mindmap is not None
    assert mindmap.root_node is not None
    assert mindmap.root_node.title == "Sports"

    # Verify there are 4 main categories
    assert len(mindmap.root_node.children) == 4

    # Verify child node titles
    child_titles = [child.title for child in mindmap.root_node.children]
    assert "Ball Sports" in child_titles
    assert "Water Sports" in child_titles
    assert "Individual Sports" in child_titles
    assert "Combat Sports" in child_titles

    # Verify Ball Sports child nodes
    ball_sports = next(child for child in mindmap.root_node.children if child.title == "Ball Sports")
    assert len(ball_sports.children) == 3
    ball_sports_titles = [child.title for child in ball_sports.children]
    assert "Basketball" in ball_sports_titles
    assert "Soccer" in ball_sports_titles
    assert "Tennis" in ball_sports_titles

    # Verify Water Sports child nodes
    water_sports = next(child for child in mindmap.root_node.children if child.title == "Water Sports")
    assert len(water_sports.children) == 2
    water_sports_titles = [child.title for child in water_sports.children]
    assert "Swimming" in water_sports_titles
    assert "Boating" in water_sports_titles

    # Verify Individual Sports child nodes
    individual_sports = next(child for child in mindmap.root_node.children if child.title == "Individual Sports")
    assert len(individual_sports.children) == 2
    individual_sports_titles = [child.title for child in individual_sports.children]
    assert "Running" in individual_sports_titles
    assert "Gymnastics" in individual_sports_titles

    # Verify Combat Sports child nodes
    combat_sports = next(child for child in mindmap.root_node.children if child.title == "Combat Sports")
    assert len(combat_sports.children) == 2
    combat_sports_titles = [child.title for child in combat_sports.children]
    assert "Boxing" in combat_sports_titles
    assert "Judo" in combat_sports_titles
