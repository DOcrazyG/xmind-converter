"""JSON conversion logic"""

import json
from typing import Dict, Any
from ..models import MindMap
from .base_converter import BaseConverter


class JSONConverter(BaseConverter):
    """JSON converter"""

    def convert_to(self, mindmap: MindMap, output_path: str) -> None:
        """Convert XMind nodes to JSON file"""

        # Build node dictionary
        def build_node_dict(current_node) -> Dict[str, Any]:
            node_dict: Dict[str, Any] = {
                "id": current_node.id,
                "title": current_node.title,
                "children": [],
            }

            if current_node.notes:
                node_dict["notes"] = current_node.notes

            if current_node.labels:
                node_dict["labels"] = current_node.labels

            for child in current_node.children:
                node_dict["children"].append(build_node_dict(child))

            return node_dict

        mindmap_dict: Dict[str, Any] = {
            "title": mindmap.title,
            "topic_node": None,
            "detached_nodes": [],
            "relations": [],
        }

        if mindmap.topic_node:
            mindmap_dict["topic_node"] = build_node_dict(mindmap.topic_node)

        for detached_node in mindmap.detached_nodes:
            mindmap_dict["detached_nodes"].append(build_node_dict(detached_node))

        for relation in mindmap.relations:
            mindmap_dict["relations"].append(
                {
                    "id": relation.id,
                    "source_id": relation.source_id,
                    "target_id": relation.target_id,
                    "title": relation.title,
                }
            )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(mindmap_dict, f, ensure_ascii=False, indent=2)
            f.write("\n")
