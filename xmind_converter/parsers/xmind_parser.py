"""XMind file parser"""

import zipfile
import xml.etree.ElementTree as ET
import tempfile
import os
from typing import Dict, List, Optional, Any
from ..models import MindMap, MindNode
from ..exceptions import XMindParserError


class XMindParser:
    """XMind file parser"""

    def parse(self, file_path: str) -> MindMap:
        """Parse XMind file"""
        if not os.path.exists(file_path):
            raise XMindParserError(f"File not found: {file_path}")

        if not zipfile.is_zipfile(file_path):
            raise XMindParserError(f"Not a valid XMind file: {file_path}")

        try:
            # Extract XMind file
            with tempfile.TemporaryDirectory() as tmpdir:
                with zipfile.ZipFile(file_path, "r") as zf:
                    zf.extractall(tmpdir)

                # First try to parse content.json
                content_json_path = os.path.join(tmpdir, "content.json")
                if os.path.exists(content_json_path):
                    return self._parse_content_json(content_json_path)

                # If no content.json, try to parse content.xml
                content_xml_path = os.path.join(tmpdir, "content.xml")
                if os.path.exists(content_xml_path):
                    return self._parse_content_xml(content_xml_path)

                # If neither file exists, raise exception
                raise XMindParserError("XMind file missing content.json or content.xml")
        except Exception as e:
            raise XMindParserError(f"Failed to parse XMind file: {str(e)}")

    def _parse_content_json(self, json_path: str) -> MindMap:
        """Parse content.json file"""
        import json

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Support both formats: list (XMind 2024+) and dict with "sheets" key (older format)
        if isinstance(data, list):
            sheets: List[Dict[str, Any]] = data
        else:
            sheets = data.get("sheets", [])

        if not sheets:
            raise XMindParserError("No mind map found in XMind file")

        sheet = sheets[0]
        sheet_name = sheet.get("title", "Untitled")

        # Find root node
        root_topic = sheet.get("rootTopic")
        if root_topic is None:
            raise XMindParserError("No root node found in XMind file")

        # Parse root node
        root_node = self._parse_topic_json(root_topic)

        # Create and return MindMap object
        mindmap = MindMap(name=sheet_name, root_node=root_node)
        return mindmap

    def _parse_topic_json(self, topic_data: Dict[str, Any]) -> MindNode:
        """Parse single topic node (JSON format)"""
        # Get node id
        node_id = topic_data.get("id")

        # Get node title and clean it
        title = topic_data.get("title", "")
        title = title.replace("\u200b", "").strip()

        # Create node
        node = MindNode(title, node_id=node_id)

        # Parse child nodes - support both "topics" and "attached" keys
        children = topic_data.get("children", {})
        child_topics = children.get("topics", []) or children.get("attached", [])

        for child_topic in child_topics:
            child_node = self._parse_topic_json(child_topic)
            node.add_child(child_node)

        return node

    def _parse_content_xml(self, xml_path: str) -> MindMap:
        """Parse content.xml file"""
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Handle XML namespace
        ns = {"xmap": "urn:xmind:xmap:xmlns:content:2.0"}

        # Find first mind map - try both with and without namespace
        sheet_elem = root.find(".//sheet") or root.find(".//xmap:sheet", ns)
        if sheet_elem is None:
            raise XMindParserError("No mind map found in XMind file")

        # Get mind map name
        sheet_name = sheet_elem.get("title", "Untitled")

        # Find root node - try both with and without namespace
        root_topic_elem = sheet_elem.find(".//topic") or sheet_elem.find(".//xmap:topic", ns)
        if root_topic_elem is None:
            raise XMindParserError("No root node found in XMind file")

        # Parse root node
        root_node = self._parse_topic(root_topic_elem, ns)

        # Create and return MindMap object
        mindmap = MindMap(name=sheet_name, root_node=root_node)
        return mindmap

    def _parse_topic(self, topic_elem: ET.Element, ns: Optional[Dict[str, str]] = None) -> MindNode:
        """Parse single topic node"""
        # Get node id
        node_id = topic_elem.get("id")

        # Get node title
        title_elem = topic_elem.find("title") or (topic_elem.find("xmap:title", ns) if ns else None)
        title = title_elem.text if title_elem is not None and title_elem.text else ""
        title = title.replace("\u200b", "").strip()

        # Create node
        node = MindNode(title, node_id=node_id)

        # Parse child nodes - handle both topics and attached topics
        children_elem = topic_elem.find("children") or (topic_elem.find("xmap:children", ns) if ns else None)
        if children_elem is not None:
            topics_elem = children_elem.find("topics") or (children_elem.find("xmap:topics", ns) if ns else None)
            if topics_elem is not None:
                for child_topic_elem in topics_elem.findall("topic") or (
                    topics_elem.findall("xmap:topic", ns) if ns else []
                ):
                    child_node = self._parse_topic(child_topic_elem, ns)
                    node.add_child(child_node)

        return node
