"""XMind file parser"""

import zipfile
import xml.etree.ElementTree as ET
import tempfile
import os
from ..models import MindMap, MindNode
from ..exceptions import XMindParserError


class XMindParser:
    """XMind file parser"""

    def parse(self, file_path):
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

    def _parse_content_json(self, json_path):
        """Parse content.json file"""
        import json

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Find first mind map
        sheets = data.get("sheets", [])
        if not sheets:
            raise XMindParserError("No mind map found in XMind file")

        sheet = sheets[0]
        sheet_name = sheet.get("title", "Untitled")

        # Find root node
        root_topic = sheet.get("rootTopic")
        if not root_topic:
            raise XMindParserError("No root node found in XMind file")

        # Parse root node
        root_node = self._parse_topic_json(root_topic)

        # Create and return MindMap object
        mindmap = MindMap(name=sheet_name, root_node=root_node)
        return mindmap

    def _parse_topic_json(self, topic_data):
        """Parse single topic node (JSON format)"""
        # Get node title
        title = topic_data.get("title", "")

        # Create node
        node = MindNode(title)

        # Parse child nodes
        children = topic_data.get("children", {})
        for child_topic in children.get("topics", []):
            child_node = self._parse_topic_json(child_topic)
            node.add_child(child_node)

        return node

    def _parse_content_xml(self, xml_path):
        """Parse content.xml file"""
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Find first mind map
        sheet_elem = root.find(".//sheet")
        if not sheet_elem:
            raise XMindParserError("No mind map found in XMind file")

        # Get mind map name
        sheet_name = sheet_elem.get("title", "Untitled")

        # Find root node
        root_topic_elem = sheet_elem.find(".//topic")
        if not root_topic_elem:
            raise XMindParserError("No root node found in XMind file")

        # Parse root node
        root_node = self._parse_topic(root_topic_elem)

        # Create and return MindMap object
        mindmap = MindMap(name=sheet_name, root_node=root_node)
        return mindmap

    def _parse_topic(self, topic_elem):
        """Parse single topic node"""
        # Get node title
        title_elem = topic_elem.find("title")
        title = title_elem.text if title_elem is not None and title_elem.text else ""

        # Create node
        node = MindNode(title)

        # Parse child nodes
        for child_topic_elem in topic_elem.findall("children/topic"):
            child_node = self._parse_topic(child_topic_elem)
            node.add_child(child_node)

        return node
