"""Markdown conversion logic"""

from typing import Optional
from ..models import MindMap
from .base_converter import BaseConverter


class MarkdownConverter(BaseConverter):
    """Markdown converter"""

    def convert_to(self, mindmap: MindMap, output_path: str) -> None:
        """Convert XMind nodes to Markdown file"""
        content_lines = []

        def write_node(current_node, level: int = 1) -> None:
            # Write current node
            prefix = "#" * level
            content_lines.append(f"{prefix} {current_node.title}")

            # Write notes if present
            if current_node.notes:
                content_lines.append(f"- notes: {current_node.notes}")

            # Write labels if present
            if current_node.labels:
                labels_str = ", ".join(current_node.labels)
                content_lines.append(f"- labels: [{labels_str}]")

            content_lines.append("")

            # Write child nodes
            if current_node.children:
                for child in current_node.children:
                    write_node(child, level + 1)

        if mindmap.topic_node:
            write_node(mindmap.topic_node)
            # Remove trailing empty line
            if content_lines and content_lines[-1] == "":
                content_lines.pop()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content_lines))
            f.write("\n")
