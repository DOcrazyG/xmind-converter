"""XMind file converter"""

import json
import zipfile
import tempfile
import os
from typing import Dict, List, Any
from ..models import MindMap, MindNode
from .base_converter import BaseConverter


class XMindConverter(BaseConverter):
    """XMind file converter"""

    def convert_to(self, mindmap: MindMap, output_path: str) -> None:
        """Convert MindMap to XMind file

        Args:
            mindmap: MindMap object to convert
            output_path: Path to save XMind file
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Build content.json structure
            content_data = self._build_content_json(mindmap)

            # Write content.json
            content_json_path = os.path.join(tmpdir, "content.json")
            with open(content_json_path, "w", encoding="utf-8") as f:
                json.dump(content_data, f, ensure_ascii=False, indent=2)

            # Create XMind file as zip
            with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(content_json_path, "content.json")

    def _build_content_json(self, mindmap: MindMap) -> List[Dict[str, Any]]:
        """Build content.json structure from MindMap

        Args:
            mindmap: MindMap object

        Returns:
            List of sheets in XMind format
        """
        sheets = []

        if mindmap.root_node:
            sheet = {
                "id": self._generate_id(),
                "title": mindmap.name,
                "rootTopic": self._build_topic_json(mindmap.root_node),
            }
            sheets.append(sheet)

        return sheets

    def _build_topic_json(self, node: MindNode) -> Dict[str, Any]:
        """Build topic JSON structure from MindNode

        Args:
            node: MindNode object

        Returns:
            Topic dictionary in XMind format
        """
        topic = {
            "id": node.id or self._generate_id(),
            "title": node.title,
            "children": {"attached": []},
        }

        for child in node.children:
            topic["children"]["attached"].append(self._build_topic_json(child))

        return topic

    def _generate_id(self) -> str:
        """Generate unique ID for XMind elements

        Returns:
            Unique ID string
        """
        import uuid

        return str(uuid.uuid4())
