"""CSV conversion logic"""

import csv
from typing import Optional
from ..models import MindMap
from .base_converter import BaseConverter


class CSVConverter(BaseConverter):
    """CSV converter"""

    def convert_to(self, mindmap: MindMap, output_path: str, delimiter: str = ",") -> None:
        """Convert XMind nodes to CSV file (triples)"""
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=delimiter, lineterminator="\n")

            # Write header
            writer.writerow(["parent", "child", "relationship"])

            # Traverse node tree, generate triples
            def generate_triples(current_node, parent_title: Optional[str] = None) -> None:
                if parent_title:
                    writer.writerow([parent_title, current_node.title, "contains"])
                for child in current_node.children:
                    generate_triples(child, current_node.title)

            if mindmap.topic_node:
                generate_triples(mindmap.topic_node)
