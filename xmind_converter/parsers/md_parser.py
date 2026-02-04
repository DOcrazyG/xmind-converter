"""Markdown file parser"""

import os
from ..models import MindMap, MindNode
from ..exceptions import ParserError, FileNotFoundError
from .base_parser import BaseParser


class MarkdownParser(BaseParser):
    """Markdown file parser"""

    def parse(self, file_path: str) -> MindMap:
        """Parse Markdown file and return MindMap object

        Args:
            file_path: Path to Markdown file to parse

        Returns:
            MindMap object created from Markdown file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
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
        except Exception as e:
            raise ParserError(f"Failed to parse Markdown file: {str(e)}")
