"""HTML conversion logic"""

from ..models import MindMap
from .base_converter import BaseConverter


class HTMLConverter(BaseConverter):
    """HTML converter"""

    def convert_to(self, mindmap: MindMap, output_path: str) -> None:
        """Convert XMind nodes to HTML file"""
        with open(output_path, "w", encoding="utf-8") as f:
            # Write HTML header
            f.write("<!DOCTYPE html>\n")
            f.write('<html lang="en">\n')
            f.write("<head>\n")
            f.write('    <meta charset="UTF-8">\n')
            f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            f.write(f"    <title>{mindmap.name}</title>\n")
            f.write("    <style>\n")
            f.write("        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }\n")
            f.write("        .mindmap { margin: 20px 0; }\n")
            f.write("        .node { margin: 10px 0; }\n")
            f.write("        .children { margin-left: 20px; }\n")
            f.write("        .root { font-size: 1.5em; font-weight: bold; }\n")
            f.write("        .level-1 { font-size: 1.2em; font-weight: bold; }\n")
            f.write("        .level-2 { font-size: 1.1em; font-weight: bold; }\n")
            f.write("    </style>\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write(f"    <h1>{mindmap.name}</h1>\n")
            f.write('    <div class="mindmap">\n')

            # Write node tree
            def write_node(current_node, level=0):
                node_class = f"node level-{level}"
                if level == 0:
                    node_class += " root"

                f.write(f'    <div class="{node_class}">\n')
                f.write(f"        {current_node.title}\n")

                if current_node.children:
                    f.write('        <div class="children">\n')
                    for child in current_node.children:
                        write_node(child, level + 1)
                    f.write("        </div>\n")

                f.write("    </div>\n")

            if mindmap.root_node:
                write_node(mindmap.root_node)

            # Write HTML footer
            f.write("    </div>\n")
            f.write("</body>\n")
            f.write("</html>\n")
