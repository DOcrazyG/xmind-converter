"""HTML file parser"""

import os
from html.parser import HTMLParser as StdHTMLParser
from ..models import MindMap, MindNode
from ..exceptions import ParserError, FileNotFoundError
from .base_parser import BaseParser


class HTMLParser(BaseParser, StdHTMLParser):
    """HTML file parser - supports h1-hn tag hierarchy"""

    def __init__(self):
        BaseParser.__init__(self)
        StdHTMLParser.__init__(self)
        self.mindmap_name = None
        self.node_stack = []
        self.root_node = None
        self.current_text = ""
        self.current_level = 0

    def parse(self, file_path: str) -> MindMap:
        """Parse HTML file and return MindMap object

        Args:
            file_path: Path to HTML file to parse

        Returns:
            MindMap object created from HTML file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            self.reset()
            self.feed(html_content)

            mindmap_name = self.mindmap_name or "From HTML"
            return MindMap(name=mindmap_name, root_node=self.root_node)
        except Exception as e:
            raise ParserError(f"Failed to parse HTML file: {str(e)}")

    def handle_starttag(self, tag, attrs):
        if tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
            level = int(tag[1])
            self.current_level = level
            self.current_text = ""

    def handle_endtag(self, tag):
        if tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
            level = int(tag[1])
            if level == 1:
                self.mindmap_name = self.current_text.strip()
                self.root_node = MindNode(self.current_text.strip())
                self.node_stack = [self.root_node]
            else:
                self._finish_current_node()
            self.current_text = ""

    def handle_data(self, data):
        if data.strip() and self.current_level > 0:
            self.current_text += data

    def _finish_current_node(self):
        """Finish processing current node and add to tree based on h tag level"""
        node_title = self.current_text.strip()
        if node_title:
            new_node = MindNode(node_title)

            if self.node_stack:
                while len(self.node_stack) >= self.current_level:
                    self.node_stack.pop()

                if self.node_stack:
                    parent_node = self.node_stack[-1]
                    parent_node.add_child(new_node)
                    self.node_stack.append(new_node)
