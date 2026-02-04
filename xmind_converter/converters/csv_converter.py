"""CSV conversion logic"""

import csv
from io import StringIO
from ..models import MindMap, MindNode


class CSVConverter:
    """CSV converter"""

    def convert(self, mindmap, delimiter=","):
        """Convert XMind nodes to CSV format (triples)"""
        output = StringIO()
        writer = csv.writer(output, delimiter=delimiter, lineterminator="\n")

        # Write header
        writer.writerow(["parent", "child", "relationship"])

        # Traverse node tree, generate triples
        def generate_triples(current_node, parent_title=None):
            if parent_title:
                writer.writerow([parent_title, current_node.title, "contains"])
            for child in current_node.children:
                generate_triples(child, current_node.title)

        if mindmap.root_node:
            generate_triples(mindmap.root_node)

        return output.getvalue()

    def convert_from(self, input_path, delimiter=","):
        """Convert from CSV format to XMind nodes"""
        # Read CSV file
        triples = []
        with open(input_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=delimiter)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    triples.append((row[0], row[1]))

        # Build node tree
        node_map = {}
        root_node = None

        # First create all nodes
        for parent_title, child_title in triples:
            if parent_title not in node_map:
                node_map[parent_title] = MindNode(parent_title)
            if child_title not in node_map:
                node_map[child_title] = MindNode(child_title)

        # Then establish parent-child relationships
        for parent_title, child_title in triples:
            parent_node = node_map[parent_title]
            child_node = node_map[child_title]
            if child_node not in parent_node.children:
                parent_node.add_child(child_node)
            # Assume the parent node of the first triple is the root node
            if root_node is None:
                root_node = parent_node

        # Create and return MindMap object
        mindmap = MindMap(name="From CSV", root_node=root_node)
        return mindmap
