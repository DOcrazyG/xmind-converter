"""Data models"""

import uuid
from typing import List, Optional, Callable, Dict, Any


class Node:
    """Base node class for mind map"""

    def __init__(
        self,
        title: str,
        node_id: Optional[str] = None,
        children: Optional[List["Node"]] = None,
        notes: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> None:
        self.id: str = node_id or str(uuid.uuid4())
        self.title: str = title
        self.children: List["Node"] = children or []
        self.notes: Optional[str] = notes
        self.labels: List[str] = labels or []

    def add_child(self, child: "Node") -> None:
        """Add child node"""
        self.children.append(child)

    def remove_child(self, child: "Node") -> None:
        """Remove child node"""
        if child in self.children:
            self.children.remove(child)

    def add_label(self, label: str) -> None:
        """Add label"""
        if label not in self.labels:
            self.labels.append(label)

    def remove_label(self, label: str) -> None:
        """Remove label"""
        if label in self.labels:
            self.labels.remove(label)

    def __str__(self) -> str:
        """String representation of node"""
        return f"Node(id={self.id[:8]}..., title='{self.title}', children={len(self.children)})"

    def __repr__(self) -> str:
        """Detailed representation of node"""
        return f"Node(id='{self.id}', title='{self.title}', children={len(self.children)}, notes={self.notes is not None}, labels={self.labels})"


class TopicNode(Node):
    """Root node of structured mind tree"""

    def __init__(
        self,
        title: str,
        node_id: Optional[str] = None,
        children: Optional[List[Node]] = None,
        notes: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> None:
        super().__init__(title, node_id, children, notes, labels)

    def get_depth(self) -> int:
        """Get node depth"""

        def calculate_depth(node: Node) -> int:
            if not node.children:
                return 1
            return 1 + max(calculate_depth(child) for child in node.children)

        return calculate_depth(self)

    @property
    def depth(self) -> int:
        """Get node depth (property)"""
        return self.get_depth()

    def traverse(self, callback: Callable[[Node, int], None], depth: int = 0) -> None:
        """Traverse node tree"""
        callback(self, depth)
        for child in self.children:
            child.traverse(callback, depth + 1)

    def __str__(self) -> str:
        """String representation of topic node"""
        return f"TopicNode(id={self.id[:8]}..., title='{self.title}', children={len(self.children)}, depth={self.get_depth()})"

    def __repr__(self) -> str:
        """Detailed representation of topic node"""
        return f"TopicNode(id='{self.id}', title='{self.title}', children={len(self.children)}, depth={self.get_depth()}, notes={self.notes is not None}, labels={self.labels})"

    def print_tree(self, indent: int = 0, prefix: str = "") -> None:
        """Print node tree structure"""
        print(f"{'  ' * indent}{prefix}{self.title}")
        if self.notes:
            print(f"{'  ' * indent}  notes: {self.notes}")
        if self.labels:
            print(f"{'  ' * indent}  labels: {self.labels}")
        for i, child in enumerate(self.children):
            is_last = i == len(self.children) - 1
            child_prefix = "└── " if is_last else "├── "
            if isinstance(child, TopicNode):
                child.print_tree(indent + 1, child_prefix)
            else:
                print(f"{'  ' * (indent + 1)}{child_prefix}{child.title}")
                if child.notes:
                    print(f"{'  ' * (indent + 1)}    notes: {child.notes}")
                if child.labels:
                    print(f"{'  ' * (indent + 1)}    labels: {child.labels}")


class DetachedNode(Node):
    """Free topic node not in structured tree"""

    def __init__(
        self,
        title: str,
        node_id: Optional[str] = None,
        children: Optional[List[Node]] = None,
        notes: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> None:
        super().__init__(title, node_id, children, notes, labels)

    def __str__(self) -> str:
        """String representation of detached node"""
        return f"DetachedNode(id={self.id[:8]}..., title='{self.title}', children={len(self.children)})"

    def __repr__(self) -> str:
        """Detailed representation of detached node"""
        return f"DetachedNode(id='{self.id}', title='{self.title}', children={len(self.children)}, notes={self.notes is not None}, labels={self.labels})"


class Relation:
    """Relation between two nodes"""

    def __init__(
        self,
        source_id: str,
        target_id: str,
        relation_id: Optional[str] = None,
        title: str = "Relation",
    ) -> None:
        self.id: str = relation_id or str(uuid.uuid4())
        self.source_id: str = source_id
        self.target_id: str = target_id
        self.title: str = title

    def __str__(self) -> str:
        """String representation of relation"""
        return f"Relation(id={self.id[:8]}..., source={self.source_id[:8]}..., target={self.target_id[:8]}...)"

    def __repr__(self) -> str:
        """Detailed representation of relation"""
        return f"Relation(id='{self.id}', source_id='{self.source_id}', target_id='{self.target_id}', title='{self.title}')"


class MindMap:
    """Mind map with topic node, detached nodes and relations"""

    def __init__(
        self,
        title: Optional[str] = None,
        topic_node: Optional[TopicNode] = None,
        detached_nodes: Optional[List[DetachedNode]] = None,
        relations: Optional[List[Relation]] = None,
    ) -> None:
        self.title: str = title or "Untitled"
        self.topic_node: Optional[TopicNode] = topic_node
        self.detached_nodes: List[DetachedNode] = detached_nodes or []
        self.relations: List[Relation] = relations or []

    def get_depth(self) -> int:
        """Get mind map depth"""
        if not self.topic_node:
            return 0
        return self.topic_node.get_depth()

    @property
    def depth(self) -> int:
        """Get mind map depth (property)"""
        return self.get_depth()

    def traverse(self, callback: Callable[[Node, int], None]) -> None:
        """Traverse mind map"""
        if self.topic_node:
            self.topic_node.traverse(callback)

    def add_detached_node(self, node: DetachedNode) -> None:
        """Add detached node"""
        self.detached_nodes.append(node)

    def remove_detached_node(self, node: DetachedNode) -> None:
        """Remove detached node"""
        if node in self.detached_nodes:
            self.detached_nodes.remove(node)

    def add_relation(self, relation: Relation) -> None:
        """Add relation"""
        self.relations.append(relation)

    def remove_relation(self, relation: Relation) -> None:
        """Remove relation"""
        if relation in self.relations:
            self.relations.remove(relation)

    def get_node_by_id(self, node_id: str) -> Optional[Node]:
        """Get node by id"""
        if self.topic_node and self.topic_node.id == node_id:
            return self.topic_node

        def find_in_tree(node: Node, target_id: str) -> Optional[Node]:
            if node.id == target_id:
                return node
            for child in node.children:
                result = find_in_tree(child, target_id)
                if result:
                    return result
            return None

        if self.topic_node:
            result = find_in_tree(self.topic_node, node_id)
            if result:
                return result

        for node in self.detached_nodes:
            if node.id == node_id:
                return node
            result = find_in_tree(node, node_id)
            if result:
                return result

        return None

    def __str__(self) -> str:
        """String representation of mind map"""
        return f"MindMap(title='{self.title}', depth={self.get_depth()}, topic_node={self.topic_node.title if self.topic_node else None}, detached_nodes={len(self.detached_nodes)}, relations={len(self.relations)})"

    def __repr__(self) -> str:
        """Detailed representation of mind map"""
        return f"MindMap(title='{self.title}', depth={self.get_depth()}, topic_node={repr(self.topic_node) if self.topic_node else None}, detached_nodes={len(self.detached_nodes)}, relations={len(self.relations)})"

    def print_tree(self) -> None:
        """Print mind map tree structure"""
        print(f"Mind Map: {self.title}")
        print(f"Depth: {self.get_depth()}")
        print(f"Topic Node: {self.topic_node.title if self.topic_node else 'None'}")
        print(f"Detached Nodes: {len(self.detached_nodes)}")
        print(f"Relations: {len(self.relations)}")
        print("-" * 50)
        if self.topic_node:
            self.topic_node.print_tree()
        if self.detached_nodes:
            print("\nDetached Nodes:")
            for node in self.detached_nodes:
                print(f"  - {node.title}")
        if self.relations:
            print("\nRelations:")
            for relation in self.relations:
                print(f"  - {relation}")
