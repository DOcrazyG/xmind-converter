"""Markdown conversion logic"""

from io import StringIO
from ..models import MindMap, MindNode
from .base_converter import BaseConverter


class MarkdownConverter(BaseConverter):
    """Markdown converter"""

    def convert_to(self, mindmap: MindMap) -> str:
        """Convert XMind nodes to Markdown format"""
        output = StringIO()

        def write_node(current_node, level=1):
            # Write current node
            prefix = "#" * level
            output.write(f"{prefix} {current_node.title}\n\n")

            # Write child nodes
            if current_node.children:
                for child in current_node.children:
                    write_node(child, level + 1)

        if mindmap.root_node:
            write_node(mindmap.root_node)

        return output.getvalue()

    def convert_from(self, input_path: str) -> MindMap:
        """Convert from Markdown format to XMind nodes"""
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Build node tree
        node_stack = []
        root_node = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if it's a header line
            if line.startswith("#"):
                # Calculate header level
                level = 0
                while line.startswith("#"):
                    level += 1
                    line = line[1:].strip()

                # Create new node
                new_node = MindNode(line)

                # Handle node relationships
                while node_stack and len(node_stack) >= level:
                    node_stack.pop()

                if node_stack:
                    # Add as child of parent node
                    parent_node = node_stack[-1]
                    parent_node.add_child(new_node)
                else:
                    # Root node
                    root_node = new_node

                # Add new node to stack
                node_stack.append(new_node)

        # Create and return MindMap object
        mindmap = MindMap(name="From Markdown", root_node=root_node)
        return mindmap
