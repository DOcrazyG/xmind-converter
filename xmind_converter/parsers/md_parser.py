"""Markdown file parser"""

import os
from typing import List, Optional
from ..models import MindMap, TopicNode
from ..exceptions import ParserError, FileNotFound
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
            raise FileNotFound(f"File not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Build node tree
            node_stack: List[TopicNode] = []
            root_node: Optional[TopicNode] = None
            i = 0

            while i < len(lines):
                line = lines[i].strip()
                if not line:
                    i += 1
                    continue

                # Check if it's a header line
                if line.startswith("#"):
                    # Calculate header level
                    level = 0
                    while line.startswith("#"):
                        level += 1
                        line = line[1:].strip()

                    # Create new node
                    new_node = TopicNode(line)

                    # Check for notes and labels in following lines
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        if next_line.startswith("- notes:"):
                            notes = next_line[len("- notes:") :].strip()
                            new_node.notes = notes
                            j += 1
                        elif next_line.startswith("- labels:"):
                            labels_str = next_line[len("- labels:") :].strip()
                            # Parse labels from format [label1, label2]
                            if labels_str.startswith("[") and labels_str.endswith("]"):
                                labels_str = labels_str[1:-1]
                                labels = [label.strip() for label in labels_str.split(",") if label.strip()]
                                new_node.labels = labels
                            j += 1
                        elif next_line.startswith("#") or not next_line:
                            break
                        else:
                            j += 1

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

                    i = j
                else:
                    i += 1

            # Create and return MindMap object
            mindmap = MindMap(title="From Markdown", topic_node=root_node)
            return mindmap
        except Exception as e:
            raise ParserError(f"Failed to parse Markdown file: {str(e)}")
