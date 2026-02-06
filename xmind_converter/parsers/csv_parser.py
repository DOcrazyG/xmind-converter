"""CSV file parser"""

import csv
import os
from typing import List, Tuple, Dict, Optional
from ..models import MindMap, MindNode
from ..exceptions import ParserError, FileNotFound
from .base_parser import BaseParser


class CSVParser(BaseParser):
    """CSV file parser"""

    def parse(self, file_path: str, delimiter: str = ",") -> MindMap:
        """Parse CSV file and return MindMap object

        Args:
            file_path: Path to CSV file to parse
            delimiter: CSV delimiter character (default: ",")

        Returns:
            MindMap object created from CSV file
        """
        if not os.path.exists(file_path):
            raise FileNotFound(f"File not found: {file_path}")

        try:
            triples: List[Tuple[str, str]] = []
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=delimiter)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        triples.append((row[0], row[1]))

            # Build node tree
            node_map: Dict[str, MindNode] = {}
            root_node: Optional[MindNode] = None

            # First create all nodes
            for parent_title, child_title in triples:
                if parent_title not in node_map:
                    node_map[parent_title] = MindNode(parent_title)
                if child_title not in node_map:
                    node_map[child_title] = MindNode(child_title)

            # Then establish parent-child relationships
            for parent_title, child_title in triples:
                parent_node = node_map[parent_title]
                child_node = node_map[child_title]
                if child_node not in parent_node.children:
                    parent_node.add_child(child_node)
                # Assume parent node of first triple is the root node
                if root_node is None:
                    root_node = parent_node

            # Create and return MindMap object
            mindmap = MindMap(name="From CSV", root_node=root_node)
            return mindmap
        except Exception as e:
            raise ParserError(f"Failed to parse CSV file: {str(e)}")
