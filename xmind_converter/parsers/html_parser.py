"""HTML file parser"""

from html.parser import HTMLParser as StdHTMLParser
from ..models import MindMap, MindNode
from .base_parser import BaseParser


class HTMLParser(BaseParser, StdHTMLParser):
    """HTML file parser"""

    def __init__(self):
        BaseParser.__init__(self)
        StdHTMLParser.__init__(self)
        self.mindmap_name = None
        self.node_stack = []
        self.root_node = None
        self.current_text = ""
        self.in_h1 = False
        self.in_node = False
        self.div_stack = []

    def parse(self, file_path: str) -> MindMap:
        """Parse HTML file and return MindMap object

        Args:
            file_path: Path to the HTML file to parse

        Returns:
            MindMap object created from the HTML file
        """
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        self.reset()
        self.feed(html_content)

        mindmap_name = self.mindmap_name or "From HTML"
        return MindMap(name=mindmap_name, root_node=self.root_node)

    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            self.in_h1 = True
            self.current_text = ""
        elif tag == "div":
            attrs_dict = dict(attrs)
            class_attr = attrs_dict.get("class", "")
            self.div_stack.append(class_attr)

            if "node" in class_attr and "children" not in class_attr:
                self.in_node = True
                self.current_text = ""

    def handle_endtag(self, tag):
        if tag == "h1" and self.in_h1:
            self.mindmap_name = self.current_text.strip()
            self.in_h1 = False
            self.current_text = ""
        elif tag == "div":
            if self.div_stack:
                current_class = self.div_stack.pop()

                if self.in_node and "node" in current_class and "children" not in current_class:
                    node_title = self.current_text.strip()
                    if node_title:
                        new_node = MindNode(node_title)

                        if self.node_stack:
                            parent_node = self.node_stack[-1]
                            parent_node.add_child(new_node)
                        else:
                            self.root_node = new_node

                        self.node_stack.append(new_node)

                    self.in_node = False
                    self.current_text = ""
                elif "node" in current_class and "children" not in current_class:
                    if self.node_stack:
                        self.node_stack.pop()

    def handle_data(self, data):
        if data.strip():
            if self.in_h1 or self.in_node:
                self.current_text += data
