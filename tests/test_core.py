"""核心功能测试"""

import pytest
from xmind_converter.core import MindMap, MindNode, CoreConverter
from xmind_converter.exceptions import XMindConverterError


def test_mind_node_creation():
    """测试节点创建"""
    node = MindNode("测试节点")
    assert node.title == "测试节点"
    assert len(node.children) == 0
    assert node.id is not None


def test_mind_node_add_child():
    """测试添加子节点"""
    parent = MindNode("父节点")
    child = MindNode("子节点")
    parent.add_child(child)
    assert len(parent.children) == 1
    assert parent.children[0] == child
    assert child.parent == parent


def test_mind_node_depth():
    """测试节点深度"""
    root = MindNode("根节点")
    assert root.get_depth() == 1

    child1 = MindNode("子节点1")
    root.add_child(child1)
    assert root.get_depth() == 1  # 根节点深度始终为1
    assert child1.get_depth() == 2

    child2 = MindNode("子节点2")
    child1.add_child(child2)
    assert child2.get_depth() == 3


def test_mind_map_creation():
    """测试思维导图创建"""
    mindmap = MindMap("测试思维导图")
    assert mindmap.name == "测试思维导图"
    assert mindmap.root_node is None


def test_mind_map_add_root_node():
    """测试添加根节点"""
    mindmap = MindMap("测试思维导图")
    root_node = MindNode("根节点")
    mindmap.add_root_node(root_node)
    assert mindmap.root_node == root_node


def test_mind_map_depth():
    """测试思维导图深度"""
    mindmap = MindMap("测试思维导图")
    assert mindmap.get_depth() == 0

    root_node = MindNode("根节点")
    mindmap.add_root_node(root_node)
    assert mindmap.get_depth() == 1

    child1 = MindNode("子节点1")
    root_node.add_child(child1)
    assert mindmap.get_depth() == 2


def test_converter_initialization():
    """测试转换器初始化"""
    converter = CoreConverter()
    assert converter is not None
    assert "csv" in converter.converters
    assert "md" in converter.converters
    assert "html" in converter.converters
    assert "json" in converter.converters


def test_unsupported_format():
    """测试不支持的格式"""
    converter = CoreConverter()
    mindmap = MindMap("测试思维导图")
    with pytest.raises(XMindConverterError):
        converter.convert_to(mindmap, "unsupported", "output.txt")
