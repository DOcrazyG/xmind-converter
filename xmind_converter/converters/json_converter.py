"""JSON conversion logic"""

import json
from ..models import MindMap, MindNode
from .base_converter import BaseConverter


class JSONConverter(BaseConverter):
    """JSON converter"""

    def convert_to(self, mindmap: MindMap) -> str:
        """Convert XMind nodes to JSON format"""

        # Build node dictionary
        def build_node_dict(current_node):
            node_dict = {"id": current_node.id, "title": current_node.title, "children": []}

            for child in current_node.children:
                node_dict["children"].append(build_node_dict(child))

            return node_dict

        mindmap_dict = {"name": mindmap.name, "root_node": None}

        if mindmap.root_node:
            mindmap_dict["root_node"] = build_node_dict(mindmap.root_node)

        return json.dumps(mindmap_dict, ensure_ascii=False, indent=2) + "\n"

    def convert_from(self, input_path: str) -> MindMap:
        """Convert from JSON format to XMind nodes"""
        with open(input_path, "r", encoding="utf-8") as f:
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
