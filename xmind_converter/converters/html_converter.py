"""HTML conversion logic"""

from typing import Optional
from ..models import MindMap
from .base_converter import BaseConverter


class HTMLConverter(BaseConverter):
    """HTML converter - outputs h1-hn tag hierarchy format"""

    def convert_to(self, mindmap: MindMap, output_path: str) -> None:
        """Convert XMind nodes to HTML file with h1-hn tag hierarchy"""
        with open(output_path, "w", encoding="utf-8") as f:
            # Write HTML header
            f.write("<!DOCTYPE html>\n")
            f.write('<html lang="en">\n')
            f.write("<head>\n")
            f.write('    <meta charset="UTF-8">\n')
            f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            f.write(f"    <title>{mindmap.title}</title>\n")
            f.write("    <style>\n")
            f.write("        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }\n")
            f.write("        h1 { font-size: 2em; font-weight: bold; }\n")
            f.write("        h2 { font-size: 1.5em; font-weight: bold; }\n")
            f.write("        h3 { font-size: 1.2em; font-weight: bold; }\n")
            f.write("        h4 { font-size: 1.1em; font-weight: bold; }\n")
            f.write("        h5 { font-size: 1em; font-weight: bold; }\n")
            f.write("        h6 { font-size: 0.9em; font-weight: bold; }\n")
            f.write("    </style>\n")
            f.write("</head>\n")
            f.write("<body>\n")

            # Write node tree with h1-hn tags
            def write_node(current_node, level: int = 1) -> None:
                h_tag = f"h{level}"
                f.write(f"    <{h_tag}>{current_node.title}</{h_tag}>\n")

                if current_node.children:
                    for child in current_node.children:
                        write_node(child, level + 1)

            if mindmap.topic_node:
                write_node(mindmap.topic_node)

            # Write HTML footer
            f.write("</body>\n")
            f.write("</html>\n")
