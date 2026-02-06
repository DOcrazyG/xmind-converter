"""Data models"""

import uuid
from typing import List, Optional, Callable


class MindNode:
    """Mind map node"""

    def __init__(
        self,
        title: str,
        node_id: Optional[str] = None,
        parent: Optional["MindNode"] = None,
        children: Optional[List["MindNode"]] = None,
    ) -> None:
        self.id: str = node_id or str(uuid.uuid4())
        self.title: str = title
        self.parent: Optional["MindNode"] = parent
        self.children: List["MindNode"] = children or []

    def add_child(self, child: "MindNode") -> None:
        """Add child node"""
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: "MindNode") -> None:
        """Remove child node"""
        if child in self.children:
            child.parent = None
            self.children.remove(child)

    def get_depth(self) -> int:
        """Get node depth"""
        if not self.parent:
            return 1
        return 1 + self.parent.get_depth()

    @property
    def depth(self) -> int:
        """Get node depth (property)"""
        return self.get_depth()

    def traverse(self, callback: Callable[["MindNode", int], None], depth: Optional[int] = None) -> None:
        """Traverse node tree"""
        if depth is None:
            depth = self.get_depth() - 1
        callback(self, depth)
        for child in self.children:
            child.traverse(callback, depth + 1)

    def __str__(self) -> str:
        """String representation of node"""
        return f"MindNode(id={self.id[:8]}..., title='{self.title}', children={len(self.children)})"

    def __repr__(self) -> str:
        """Detailed representation of node"""
        parent_id = (self.parent.id[:8] + "...") if self.parent else None
        return f"MindNode(id='{self.id}', title='{self.title}', parent={parent_id}, children={len(self.children)})"

    def print_tree(self, indent: int = 0, prefix: str = "") -> None:
        """Print node tree structure"""
        print(f"{'  ' * indent}{prefix}{self.title}")
        for i, child in enumerate(self.children):
            is_last = i == len(self.children) - 1
            child_prefix = "└── " if is_last else "├── "
            child.print_tree(indent + 1, child_prefix)


class MindMap:
    """Mind map"""

    def __init__(self, name: Optional[str] = None, root_node: Optional["MindNode"] = None) -> None:
        self.name: str = name or "Untitled"
        self.root_node: Optional["MindNode"] = root_node

    def get_depth(self) -> int:
        """Get mind map depth"""
        if not self.root_node:
            return 0

        # Calculate maximum depth of the entire tree
        def calculate_max_depth(node: MindNode) -> int:
            if not node.children:
                return 1
            return 1 + max(calculate_max_depth(child) for child in node.children)

        return calculate_max_depth(self.root_node)

    @property
    def depth(self) -> int:
        """Get mind map depth (property)"""
        return self.get_depth()

    def traverse(self, callback: Callable[["MindNode", int], None]) -> None:
        """Traverse mind map"""
        if self.root_node:
            self.root_node.traverse(callback)

    def add_root_node(self, node: "MindNode") -> None:
        """Add root node"""
        self.root_node = node

    def __str__(self) -> str:
        """String representation of mind map"""
        return f"MindMap(name='{self.name}', depth={self.get_depth()}, root_node={self.root_node.title if self.root_node else None})"

    def __repr__(self) -> str:
        """Detailed representation of mind map"""
        return f"MindMap(name='{self.name}', depth={self.get_depth()}, root_node={repr(self.root_node) if self.root_node else None})"

    def print_tree(self) -> None:
        """Print mind map tree structure"""
        print(f"Mind Map: {self.name}")
        print(f"Depth: {self.get_depth()}")
        print(f"Root: {self.root_node.title if self.root_node else 'None'}")
        print("-" * 50)
        if self.root_node:
            self.root_node.print_tree()
