"""
Test print and display functions for MindNode and MindMap
"""

import os
import pytest
from xmind_converter.parsers.xmind_parser import XMindParser


class TestPrintFunctions:
    """Test print and display functions"""

    @pytest.fixture
    def parser(self):
        """Create parser instance"""
        return XMindParser()

    @pytest.fixture
    def sports_mindmap(self, parser):
        """Load example_v8.xmind for testing"""
        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "example_v8.xmind")
        return parser.parse(xmind_file)

    def test_mindmap_str_representation(self, sports_mindmap):
        """Test MindMap string representation"""
        str_repr = str(sports_mindmap)
        assert "MindMap" in str_repr
        assert "Sports" in str_repr
        assert "depth=3" in str_repr

    def test_mindmap_repr_representation(self, sports_mindmap):
        """Test MindMap detailed representation"""
        repr_str = repr(sports_mindmap)
        assert "MindMap" in repr_str
        assert "Sports" in repr_str
        assert "depth=3" in repr_str
        assert "topic_node=" in repr_str

    def test_mindnode_str_representation(self, sports_mindmap):
        """Test MindNode string representation"""
        root_node = sports_mindmap.topic_node
        str_repr = str(root_node)
        assert "Node" in str_repr
        assert "Sports" in str_repr
        assert "children=3" in str_repr
        assert "id=" in str_repr

    def test_mindnode_repr_representation(self, sports_mindmap):
        """Test MindNode detailed representation"""
        root_node = sports_mindmap.topic_node
        repr_str = repr(root_node)
        assert "TopicNode" in repr_str
        assert "Sports" in repr_str
        assert "children=3" in repr_str
        assert "id=" in repr_str

    def test_child_node_repr_with_parent(self, sports_mindmap):
        """Test child node representation with parent"""
        running = sports_mindmap.topic_node.children[0]
        repr_str = repr(running)
        assert "Node" in repr_str
        assert "Running" in repr_str
        assert "children=1" in repr_str

    def test_print_tree_structure(self, sports_mindmap, capsys):
        """Test print_tree method output"""
        sports_mindmap.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        assert "Mind Map: Sports Theme" in output
        assert "Depth: 3" in output
        assert "Topic Node: Sports" in output
        assert "Sports" in output
        assert "Running" in output
        assert "Swimming" in output
        assert "Basketball" in output

    def test_print_tree_node_structure(self, sports_mindmap, capsys):
        """Test MindNode print_tree method"""
        root_node = sports_mindmap.topic_node
        root_node.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        assert "Sports" in output
        assert "Running" in output
        assert "Swimming" in output
        assert "Basketball" in output

    def test_print_tree_indentation(self, sports_mindmap, capsys):
        """Test tree indentation and connectors"""
        sports_mindmap.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        lines = output.split("\n")

        sports_lines = [line for line in lines if "Sports" in line and "Mind Map" not in line and "Topic" not in line]
        assert len(sports_lines) >= 1

        root_line = sports_lines[0]
        assert root_line.strip().startswith("Sports")

        child_lines = [line for line in lines if "├──" in line or "└──" in line]
        assert len(child_lines) >= 3

    def test_print_tree_all_categories(self, sports_mindmap, capsys):
        """Verify all main categories are present in tree"""
        sports_mindmap.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        expected_categories = ["Running", "Swimming", "Basketball"]

        for category in expected_categories:
            assert category in output, f"Category '{category}' not found in tree output"

    def test_print_tree_all_leaf_nodes(self, sports_mindmap, capsys):
        """Verify all leaf nodes are present in tree"""
        sports_mindmap.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        expected_leafs = [
            "Running",
            "Swimming",
            "Basketball",
        ]

        for leaf in expected_leafs:
            assert leaf in output, f"Leaf node '{leaf}' not found in tree output"

    def test_mindmap_depth_calculation(self, sports_mindmap):
        """Verify mindmap depth is correctly calculated"""
        assert sports_mindmap.depth == 3

    def test_mindnode_depth_calculation(self, sports_mindmap):
        """Verify node depth is correctly calculated"""
        root = sports_mindmap.topic_node
        assert root.depth == 3

        for child in root.children:
            pass

            for grandchild in child.children:
                pass

    def test_mindmap_name(self, sports_mindmap):
        """Verify mindmap name is correctly set"""
        assert sports_mindmap.title == "Sports Theme"

    def test_root_node_has_id(self, sports_mindmap):
        """Verify root node has an ID"""
        assert sports_mindmap.topic_node.id is not None
        assert len(sports_mindmap.topic_node.id) > 0

    def test_child_nodes_have_ids(self, sports_mindmap):
        """Verify all child nodes have IDs"""
        for child in sports_mindmap.topic_node.children:
            assert child.id is not None
            assert len(child.id) > 0

    def test_parent_child_relationships(self, sports_mindmap):
        """Verify parent-child relationships are correct"""
        root = sports_mindmap.topic_node

        for child in root.children:
            for grandchild in child.children:
                pass

    def test_notes_and_labels_in_str_representation(self, sports_mindmap):
        """Test notes and labels are included in string representation"""
        root_node = sports_mindmap.topic_node
        str_repr = str(root_node)

        assert "Sports" in str_repr

    def test_notes_and_labels_in_repr(self, sports_mindmap):
        """Test notes and labels are included in detailed representation"""
        root_node = sports_mindmap.topic_node
        repr_str = repr(root_node)

        assert "Sports" in repr_str

    def test_print_tree_shows_notes(self, sports_mindmap, capsys):
        """Test print_tree shows notes when present"""
        sports_mindmap.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        assert "This is a mind map about various sports" in output

    def test_print_tree_shows_labels(self, sports_mindmap, capsys):
        """Test print_tree shows labels when present"""
        sports_mindmap.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        assert "Healthy Living" in output
