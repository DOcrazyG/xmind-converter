"""JSON file parser"""

import json
import os
from ..models import MindMap, MindNode
from ..exceptions import ParserError, FileNotFoundError
from .base_parser import BaseParser


class JSONParser(BaseParser):
    """JSON file parser"""

    def parse(self, file_path: str) -> MindMap:
        """Parse JSON file and return MindMap object

        Args:
            file_path: Path to JSON file to parse

        Returns:
            MindMap object created from JSON file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Build node tree
            def build_node_from_dict(node_dict):
                node = MindNode(node_dict.get("title", ""), node_id=node_dict.get("id"))

                for child_dict in node_dict.get("children", []):
                    child_node = build_node_from_dict(child_dict)
                    node.add_child(child_node)

                return node

            mindmap_name = data.get("name", "From JSON")
            root_node = None

            if "root_node" in data:
                root_node = build_node_from_dict(data["root_node"])
            elif "title" in data:  # Compatible with old format
                root_node = build_node_from_dict(data)

            return MindMap(name=mindmap_name, root_node=root_node)
        except Exception as e:
            raise ParserError(f"Failed to parse JSON file: {str(e)}")
