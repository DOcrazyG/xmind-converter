"""转换器测试"""

import pytest
import tempfile
import os
from xmind_converter.core import MindMap, MindNode
from xmind_converter.converters.csv_converter import CSVConverter
from xmind_converter.converters.md_converter import MarkdownConverter
from xmind_converter.converters.html_converter import HTMLConverter
from xmind_converter.converters.json_converter import JSONConverter


def test_csv_conversion():
    """测试CSV转换"""
    # 创建测试节点和思维导图
    root = MindNode("根节点")
    child1 = MindNode("子节点1")
    child2 = MindNode("子节点2")
    root.add_child(child1)
    root.add_child(child2)
    mindmap = MindMap("测试思维导图", root_node=root)
    
    # 测试转换
    converter = CSVConverter()
    csv_content = converter.convert(mindmap)
    assert "根节点,子节点1,contains" in csv_content
    assert "根节点,子节点2,contains" in csv_content


def test_md_conversion():
    """测试Markdown转换"""
    # 创建测试节点和思维导图
    root = MindNode("根节点")
    child1 = MindNode("子节点1")
    root.add_child(child1)
    mindmap = MindMap("测试思维导图", root_node=root)
    
    # 测试转换
    converter = MarkdownConverter()
    md_content = converter.convert(mindmap)
    assert "# 根节点" in md_content
    assert "## 子节点1" in md_content


def test_html_conversion():
    """测试HTML转换"""
    # 创建测试节点和思维导图
    root = MindNode("根节点")
    mindmap = MindMap("测试思维导图", root_node=root)
    
    # 测试转换
    converter = HTMLConverter()
    html_content = converter.convert(mindmap)
    assert "<!DOCTYPE html>" in html_content
    assert "测试思维导图" in html_content
    assert "根节点" in html_content


def test_json_conversion():
    """测试JSON转换"""
    # 创建测试节点和思维导图
    root = MindNode("根节点")
    child1 = MindNode("子节点1")
    root.add_child(child1)
    mindmap = MindMap("测试思维导图", root_node=root)
    
    # 测试转换
    converter = JSONConverter()
    json_content = converter.convert(mindmap)
    assert "测试思维导图" in json_content
    assert "根节点" in json_content
    assert "子节点1" in json_content


def test_csv_reverse_conversion():
    """测试CSV反向转换"""
    # 创建测试CSV文件
    csv_content = "parent,child,relationship\n根节点,子节点1,contains\n根节点,子节点2,contains"
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        f.write(csv_content.encode('utf-8'))
        temp_file = f.name
    
    try:
        converter = CSVConverter()
        mindmap = converter.convert_from(temp_file)
        assert mindmap.name == "From CSV"
        assert mindmap.root_node.title == "根节点"
        assert len(mindmap.root_node.children) == 2
    finally:
        os.unlink(temp_file)