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

            # Write metadata.json
            metadata_data = self._build_metadata_json()
            metadata_json_path = os.path.join(tmpdir, "metadata.json")
            with open(metadata_json_path, "w", encoding="utf-8") as f:
                json.dump(metadata_data, f, ensure_ascii=False, indent=2)

            # Write manifest.json
            manifest_data = self._build_manifest_json()
            manifest_json_path = os.path.join(tmpdir, "manifest.json")
            with open(manifest_json_path, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, ensure_ascii=False, indent=2)

            # Create Thumbnails directory and write thumbnail.png
            thumbnails_dir = os.path.join(tmpdir, "Thumbnails")
            os.makedirs(thumbnails_dir, exist_ok=True)
            thumbnail_path = os.path.join(thumbnails_dir, "thumbnail.png")
            self._create_thumbnail(thumbnail_path)

            # Create XMind file as zip
            with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(content_json_path, "content.json")
                zf.write(metadata_json_path, "metadata.json")
                zf.write(manifest_json_path, "manifest.json")
                zf.write(thumbnail_path, "Thumbnails/thumbnail.png")

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
                "rootTopic": self._build_topic_json(mindmap.root_node, is_root=True),
            }
            sheets.append(sheet)

        return sheets

    def _build_topic_json(self, node: MindNode, is_root: bool = False) -> Dict[str, Any]:
        """Build topic JSON structure from MindNode

        Args:
            node: MindNode object
            is_root: Whether this is the root topic

        Returns:
            Topic dictionary in XMind format
        """
        topic = {
            "id": node.id or self._generate_id(),
            "title": node.title,
            "children": {"attached": []},
        }

        if is_root:
            topic["class"] = "topic"
            topic["structureClass"] = "org.xmind.ui.logic.right"

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

    def _build_metadata_json(self) -> Dict[str, Any]:
        """Build metadata.json structure

        Returns:
            Metadata dictionary in XMind format
        """
        return {
            "dataStructureVersion": "2",
            "creator": {"name": "xmind-converter", "version": "1.0.0"},
            "layoutEngineVersion": "3",
        }

    def _build_manifest_json(self) -> Dict[str, Any]:
        """Build manifest.json structure

        Returns:
            Manifest dictionary in XMind format
        """
        return {"file-entries": {"content.json": {}, "metadata.json": {}, "Thumbnails/thumbnail.png": {}}}

    def _create_thumbnail(self, thumbnail_path: str) -> None:
        """Create a minimal valid PNG thumbnail

        Args:
            thumbnail_path: Path to save the thumbnail PNG file
        """
        import struct

        width, height = 200, 150
        pixels = b"\x00" * (width * height * 3)

        def write_png(buf, width, height, pixels):
            buf.extend(b"\x89PNG\r\n\x1a\n")

            def chunk(name, data):
                buf.extend(struct.pack(">I", len(data)))
                buf.extend(name)
                buf.extend(data)
                buf.extend(struct.pack(">I", 0xFFFFFFFF & sum(data) % (1 << 32)))

            def IHDR():
                return struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)

            chunk(b"IHDR", IHDR())
            raw = b""
            for y in range(height):
                raw += b"\x00"
                raw += pixels[y * width * 3 : (y + 1) * width * 3]
            import zlib

            chunk(b"IDAT", zlib.compress(raw))
            chunk(b"IEND", b"")

        buf = bytearray()
        write_png(buf, width, height, pixels)
        with open(thumbnail_path, "wb") as f:
            f.write(buf)
