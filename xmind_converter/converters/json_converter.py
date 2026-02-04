"""JSON conversion logic"""

import json
from ..models import MindMap
from .base_converter import BaseConverter


class JSONConverter(BaseConverter):
    """JSON converter"""

    def convert_to(self, mindmap: MindMap, output_path: str) -> None:
        """Convert XMind nodes to JSON file"""

        # Build node dictionary
        def build_node_dict(current_node):
            node_dict = {"id": current_node.id, "title": current_node.title, "children": []}

            for child in current_node.children:
                node_dict["children"].append(build_node_dict(child))

            return node_dict

        mindmap_dict = {"name": mindmap.name, "root_node": None}

        if mindmap.root_node:
            mindmap_dict["root_node"] = build_node_dict(mindmap.root_node)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(mindmap_dict, f, ensure_ascii=False, indent=2)
            f.write("\n")
