"""XMind file parser"""

import zipfile
import xml.etree.ElementTree as ET
import tempfile
import os
from typing import Dict, List, Optional, Any
from ..models import MindMap, TopicNode, DetachedNode, Relation, Node
from ..exceptions import ParserError, FileNotFound, FileFormatError
from .base_parser import BaseParser


class XMindParser(BaseParser):
    """XMind file parser"""

    def parse(self, file_path: str) -> MindMap:
        """Parse XMind file"""
        if not os.path.exists(file_path):
            raise FileNotFound(f"File not found: {file_path}")

        if not zipfile.is_zipfile(file_path):
            raise FileFormatError(f"Not a valid XMind file: {file_path}")

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                with zipfile.ZipFile(file_path, "r") as zf:
                    zf.extractall(tmpdir)

                content_json_path = os.path.join(tmpdir, "content.json")
                if os.path.exists(content_json_path):
                    return self._parse_content_json(content_json_path)

                content_xml_path = os.path.join(tmpdir, "content.xml")
                if os.path.exists(content_xml_path):
                    return self._parse_content_xml(content_xml_path)

                raise ParserError("XMind file missing content.json or content.xml")
        except Exception as e:
            raise ParserError(f"Failed to parse XMind file: {str(e)}")

    def _parse_content_json(self, json_path: str) -> MindMap:
        """Parse content.json file"""
        import json

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            sheets: List[Dict[str, Any]] = data
        else:
            sheets = data.get("sheets", [])

        if not sheets:
            raise ParserError("No mind map found in XMind file")

        sheet = sheets[0]
        sheet_name = sheet.get("title", "Untitled")

        root_topic = sheet.get("rootTopic")
        if root_topic is None:
            raise ParserError("No root node found in XMind file")

        topic_node = self._parse_topic_json(root_topic, TopicNode)

        detached_nodes: List[DetachedNode] = []
        detached_topics = sheet.get("detachedTopics", [])
        for detached_topic in detached_topics:
            detached_node = self._parse_topic_json(detached_topic, DetachedNode)
            detached_nodes.append(detached_node)

        relations: List[Relation] = []
        relationships = sheet.get("relationships", [])
        for rel_data in relationships:
            relation = Relation(
                source_id=rel_data.get("end1Id", ""),
                target_id=rel_data.get("end2Id", ""),
                relation_id=rel_data.get("id"),
                title=rel_data.get("title", "Relation"),
            )
            relations.append(relation)

        mindmap = MindMap(
            title=sheet_name,
            topic_node=topic_node,
            detached_nodes=detached_nodes,
            relations=relations,
        )
        return mindmap

    def _parse_topic_json(self, topic_data: Dict[str, Any], node_class: type = Node) -> Node:
        """Parse single topic node (JSON format)"""
        node_id = topic_data.get("id")

        title = topic_data.get("title", "")
        title = title.replace("\u200b", "").strip()

        notes = None
        notes_data = topic_data.get("notes")
        if notes_data and isinstance(notes_data, dict):
            plain = notes_data.get("plain")
            if plain and isinstance(plain, dict):
                notes = plain.get("content")
            elif isinstance(plain, str):
                notes = plain

        labels = topic_data.get("labels", [])

        node = node_class(
            title=title,
            node_id=node_id,
            notes=notes,
            labels=labels,
        )

        children_data = topic_data.get("children", {})
        child_topics = children_data.get("attached", [])

        for child_topic in child_topics:
            child_node = self._parse_topic_json(child_topic, Node)
            node.add_child(child_node)

        return node

    def _parse_content_xml(self, xml_path: str) -> MindMap:
        """Parse content.xml file"""
        try:
            from defusedxml import ElementTree as SafeET

            tree = SafeET.parse(xml_path)
        except ImportError:
            import warnings

            warnings.warn(
                "defusedxml not installed, using standard xml.etree.ElementTree. "
                "For better security, install defusedxml: pip install defusedxml",
                UserWarning,
            )
            tree = ET.parse(xml_path)
        root = tree.getroot()

        ns = {"xmap": "urn:xmind:xmap:xmlns:content:2.0"}

        sheet_elem = root.find(".//sheet") or root.find(".//xmap:sheet", ns)
        if sheet_elem is None:
            raise ParserError("No mind map found in XMind file")

        sheet_name = sheet_elem.get("title", "Untitled")

        root_topic_elem = sheet_elem.find(".//topic") or sheet_elem.find(".//xmap:topic", ns)
        if root_topic_elem is None:
            raise ParserError("No root node found in XMind file")

        topic_node = self._parse_topic_xml(root_topic_elem, ns, TopicNode)

        detached_nodes: List[DetachedNode] = []
        detached_topic_elems = sheet_elem.findall(".//detached") or sheet_elem.findall(".//xmap:detached", ns)
        for detached_elem in detached_topic_elems:
            topic_elem = detached_elem.find("topic") or detached_elem.find("xmap:topic", ns)
            if topic_elem is not None:
                detached_node = self._parse_topic_xml(topic_elem, ns, DetachedNode)
                detached_nodes.append(detached_node)

        relations: List[Relation] = []
        relation_elems = sheet_elem.findall(".//relationship") or sheet_elem.findall(".//xmap:relationship", ns)
        for rel_elem in relation_elems:
            relation = Relation(
                source_id=rel_elem.get("end1Id", ""),
                target_id=rel_elem.get("end2Id", ""),
                relation_id=rel_elem.get("id"),
                title=rel_elem.get("title", "Relation"),
            )
            relations.append(relation)

        mindmap = MindMap(
            title=sheet_name,
            topic_node=topic_node,
            detached_nodes=detached_nodes,
            relations=relations,
        )
        return mindmap

    def _parse_topic_xml(
        self, topic_elem: ET.Element, ns: Optional[Dict[str, str]] = None, node_class: type = Node
    ) -> Node:
        """Parse single topic node"""
        node_id = topic_elem.get("id")

        title_elem = topic_elem.find("title") or (topic_elem.find("xmap:title", ns) if ns else None)
        title = title_elem.text if title_elem is not None and title_elem.text else ""
        title = title.replace("\u200b", "").strip()

        notes = None
        notes_elem = topic_elem.find("notes") or (topic_elem.find("xmap:notes", ns) if ns else None)
        if notes_elem is not None:
            plain_elem = notes_elem.find("plain") or (notes_elem.find("xmap:plain", ns) if ns else None)
            if plain_elem is not None and plain_elem.text:
                notes = plain_elem.text

        labels: List[str] = []
        labels_elem = topic_elem.find("labels") or (topic_elem.find("xmap:labels", ns) if ns else None)
        if labels_elem is not None:
            for label_elem in labels_elem.findall("label") or (labels_elem.findall("xmap:label", ns) if ns else []):
                if label_elem.text:
                    labels.append(label_elem.text)

        node = node_class(
            title=title,
            node_id=node_id,
            notes=notes,
            labels=labels,
        )

        children_elem = topic_elem.find("children") or (topic_elem.find("xmap:children", ns) if ns else None)
        if children_elem is not None:
            topics_elem = children_elem.find("topics") or (children_elem.find("xmap:topics", ns) if ns else None)
            if topics_elem is not None:
                for child_topic_elem in topics_elem.findall("topic") or (
                    topics_elem.findall("xmap:topic", ns) if ns else []
                ):
                    child_node = self._parse_topic_xml(child_topic_elem, ns, Node)
                    node.add_child(child_node)

        return node
