"""HTML conversion logic"""

from io import StringIO
from ..models import MindMap
from .base_converter import BaseConverter


class HTMLConverter(BaseConverter):
    """HTML converter"""

    def convert_to(self, mindmap: MindMap) -> str:
        """Convert XMind nodes to HTML format"""
        output = StringIO()

        # Write HTML header
        output.write("<!DOCTYPE html>\n")
        output.write('<html lang="en">\n')
        output.write("<head>\n")
        output.write('    <meta charset="UTF-8">\n')
        output.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        output.write(f"    <title>{mindmap.name}</title>\n")
        output.write("    <style>\n")
        output.write("        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }\n")
        output.write("        .mindmap { margin: 20px 0; }\n")
        output.write("        .node { margin: 10px 0; }\n")
        output.write("        .children { margin-left: 20px; }\n")
        output.write("        .root { font-size: 1.5em; font-weight: bold; }\n")
        output.write("        .level-1 { font-size: 1.2em; font-weight: bold; }\n")
        output.write("        .level-2 { font-size: 1.1em; font-weight: bold; }\n")
        output.write("    </style>\n")
        output.write("</head>\n")
        output.write("<body>\n")
        output.write(f"    <h1>{mindmap.name}</h1>\n")
        output.write('    <div class="mindmap">\n')

        # Write node tree
        def write_node(current_node, level=0):
            node_class = f"node level-{level}"
            if level == 0:
                node_class += " root"

            output.write(f'    <div class="{node_class}">\n')
            output.write(f"        {current_node.title}\n")

            if current_node.children:
                output.write('        <div class="children">\n')
                for child in current_node.children:
                    write_node(child, level + 1)
                output.write("        </div>\n")

            output.write("    </div>\n")

        if mindmap.root_node:
            write_node(mindmap.root_node)

        # Write HTML footer
        output.write("    </div>\n")
        output.write("</body>\n")
        output.write("</html>\n")

        return output.getvalue()

    def convert_from(self, input_path: str) -> MindMap:
        """Convert from HTML format to XMind nodes"""
        # Simplified implementation here, actually need to use HTML parser
        # For example, use BeautifulSoup to parse HTML structure
        raise NotImplementedError("HTML to XMind conversion not implemented yet")
