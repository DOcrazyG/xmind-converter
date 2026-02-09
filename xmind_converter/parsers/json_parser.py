"""JSON file parser"""

import json
import os
from typing import Dict, Any, Optional, List
from ..models import MindMap, TopicNode, DetachedNode, Relation, Node
from ..exceptions import ParserError, FileNotFound
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
            raise FileNotFound(f"File not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)

            # Build node tree
            def build_node_from_dict(node_dict: Dict[str, Any], node_class: type = Node) -> Node:
                node = node_class(
                    title=node_dict.get("title", ""),
                    node_id=node_dict.get("id"),
                    notes=node_dict.get("notes"),
                    labels=node_dict.get("labels", []),
                )

                for child_dict in node_dict.get("children", []):
                    child_node = build_node_from_dict(child_dict, Node)
                    node.add_child(child_node)

                return node

            mindmap_title = data.get("title") or data.get("name", "From JSON")
            topic_node: Optional[TopicNode] = None
            detached_nodes: List[DetachedNode] = []
            relations: List[Relation] = []

            if "topic_node" in data:
                topic_node = build_node_from_dict(data["topic_node"], TopicNode)
            elif "root_node" in data:
                topic_node = build_node_from_dict(data["root_node"], TopicNode)
            elif "title" in data:
                topic_node = build_node_from_dict(data, TopicNode)

            if "detached_nodes" in data:
                for detached_dict in data["detached_nodes"]:
                    detached_node = build_node_from_dict(detached_dict, DetachedNode)
                    detached_nodes.append(detached_node)

            if "relations" in data:
                for rel_dict in data["relations"]:
                    relation = Relation(
                        source_id=rel_dict.get("source_id", ""),
                        target_id=rel_dict.get("target_id", ""),
                        relation_id=rel_dict.get("id"),
                        title=rel_dict.get("title", "Relation"),
                    )
                    relations.append(relation)

            return MindMap(
                title=mindmap_title,
                topic_node=topic_node,
                detached_nodes=detached_nodes,
                relations=relations,
            )
        except Exception as e:
            raise ParserError(f"Failed to parse JSON file: {str(e)}")
