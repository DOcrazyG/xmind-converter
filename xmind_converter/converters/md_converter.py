"""Markdown conversion logic"""

from typing import Optional
from ..models import MindMap
from .base_converter import BaseConverter


class MarkdownConverter(BaseConverter):
    """Markdown converter"""

    def convert_to(self, mindmap: MindMap, output_path: str) -> None:
        """Convert XMind nodes to Markdown file"""
        with open(output_path, "w", encoding="utf-8") as f:

            def write_node(current_node, level: int = 1) -> None:
                # Write current node
                prefix = "#" * level
                f.write(f"{prefix} {current_node.title}\n\n")

                # Write child nodes
                if current_node.children:
                    for child in current_node.children:
                        write_node(child, level + 1)

            if mindmap.root_node:
                write_node(mindmap.root_node)
