"""Data models"""

import uuid


class MindNode:
    """Mind map node"""

    def __init__(self, title, node_id=None, parent=None, children=None):
        self.id = node_id or str(uuid.uuid4())
        self.title = title
        self.parent = parent
        self.children = children or []

    def add_child(self, child):
        """Add child node"""
        child.parent = self
        self.children.append(child)

    def remove_child(self, child):
        """Remove child node"""
        if child in self.children:
            child.parent = None
            self.children.remove(child)

    def get_depth(self):
        """Get node depth"""
        if not self.parent:
            return 1
        return 1 + self.parent.get_depth()

    def traverse(self, callback, depth=None):
        """Traverse node tree"""
        if depth is None:
            depth = self.get_depth() - 1
        callback(self, depth)
        for child in self.children:
            child.traverse(callback, depth + 1)


class MindMap:
    """Mind map"""

    def __init__(self, name=None, root_node=None):
        self.name = name or "Untitled"
        self.root_node = root_node

    def get_depth(self):
        """Get mind map depth"""
        if not self.root_node:
            return 0

        # Calculate maximum depth of the entire tree
        def calculate_max_depth(node):
            if not node.children:
                return 1
            return 1 + max(calculate_max_depth(child) for child in node.children)

        return calculate_max_depth(self.root_node)

    def traverse(self, callback):
        """Traverse mind map"""
        if self.root_node:
            self.root_node.traverse(callback)

    def add_root_node(self, node):
        """Add root node"""
        self.root_node = node
