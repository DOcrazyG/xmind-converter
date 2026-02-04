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
        """Load sports_v8.xmind for testing"""
        xmind_file = os.path.join(os.path.dirname(__file__), "..", "data", "sports_v8.xmind")
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
        assert "root_node=" in repr_str

    def test_mindnode_str_representation(self, sports_mindmap):
        """Test MindNode string representation"""
        root_node = sports_mindmap.root_node
        str_repr = str(root_node)
        assert "MindNode" in str_repr
        assert "Sports" in str_repr
        assert "children=4" in str_repr
        assert "id=" in str_repr

    def test_mindnode_repr_representation(self, sports_mindmap):
        """Test MindNode detailed representation"""
        root_node = sports_mindmap.root_node
        repr_str = repr(root_node)
        assert "MindNode" in repr_str
        assert "Sports" in repr_str
        assert "parent=None" in repr_str
        assert "children=4" in repr_str
        assert "id=" in repr_str

    def test_child_node_repr_with_parent(self, sports_mindmap):
        """Test child node representation with parent"""
        ball_sports = sports_mindmap.root_node.children[0]
        repr_str = repr(ball_sports)
        assert "MindNode" in repr_str
        assert "Ball Sports" in repr_str
        assert "parent=" in repr_str
        assert "children=3" in repr_str

    def test_print_tree_structure(self, sports_mindmap, capsys):
        """Test print_tree method output"""
        sports_mindmap.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        assert "Mind Map: Sports" in output
        assert "Depth: 3" in output
        assert "Root: Sports" in output
        assert "Sports" in output
        assert "Ball Sports" in output
        assert "Water Sports" in output
        assert "Individual Sports" in output
        assert "Combat Sports" in output

    def test_print_tree_node_structure(self, sports_mindmap, capsys):
        """Test MindNode print_tree method"""
        root_node = sports_mindmap.root_node
        root_node.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        assert "Sports" in output
        assert "Ball Sports" in output
        assert "Water Sports" in output
        assert "Individual Sports" in output
        assert "Combat Sports" in output
        assert "Basketball" in output
        assert "Soccer" in output
        assert "Tennis" in output

    def test_print_tree_indentation(self, sports_mindmap, capsys):
        """Test tree indentation and connectors"""
        sports_mindmap.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        lines = output.split("\n")

        sports_lines = [line for line in lines if "Sports" in line and "Mind Map" not in line and "Root" not in line]
        assert len(sports_lines) >= 5

        root_line = sports_lines[0]
        assert root_line.strip().startswith("Sports")

        child_lines = [line for line in lines if "├──" in line or "└──" in line]
        assert len(child_lines) >= 4

    def test_print_tree_all_categories(self, sports_mindmap, capsys):
        """Verify all main categories are present in tree"""
        sports_mindmap.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        expected_categories = ["Ball Sports", "Water Sports", "Individual Sports", "Combat Sports"]

        for category in expected_categories:
            assert category in output, f"Category '{category}' not found in tree output"

    def test_print_tree_all_leaf_nodes(self, sports_mindmap, capsys):
        """Verify all leaf nodes are present in tree"""
        sports_mindmap.print_tree()
        captured = capsys.readouterr()

        output = captured.out
        expected_leafs = [
            "Basketball",
            "Soccer",
            "Tennis",
            "Swimming",
            "Boating",
            "Running",
            "Gymnastics",
            "Boxing",
            "Judo",
        ]

        for leaf in expected_leafs:
            assert leaf in output, f"Leaf node '{leaf}' not found in tree output"

    def test_mindmap_depth_calculation(self, sports_mindmap):
        """Verify mindmap depth is correctly calculated"""
        assert sports_mindmap.depth == 3

    def test_mindnode_depth_calculation(self, sports_mindmap):
        """Verify node depth is correctly calculated"""
        root = sports_mindmap.root_node
        assert root.depth == 1

        for child in root.children:
            assert child.depth == 2

            for grandchild in child.children:
                assert grandchild.depth == 3

    def test_mindmap_name(self, sports_mindmap):
        """Verify mindmap name is correctly set"""
        assert sports_mindmap.name == "Sports"

    def test_root_node_has_id(self, sports_mindmap):
        """Verify root node has an ID"""
        assert sports_mindmap.root_node.id is not None
        assert len(sports_mindmap.root_node.id) > 0

    def test_child_nodes_have_ids(self, sports_mindmap):
        """Verify all child nodes have IDs"""
        for child in sports_mindmap.root_node.children:
            assert child.id is not None
            assert len(child.id) > 0

    def test_parent_child_relationships(self, sports_mindmap):
        """Verify parent-child relationships are correct"""
        root = sports_mindmap.root_node
        assert root.parent is None

        for child in root.children:
            assert child.parent is root

            for grandchild in child.children:
                assert grandchild.parent is child
