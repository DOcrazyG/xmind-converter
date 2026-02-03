"""解析器测试"""

import pytest
import os
import tempfile
import zipfile
from xmind_converter.parsers.xmind_parser import XMindParser
from xmind_converter.exceptions import XMindParserError


def test_parse_nonexistent_file():
    """测试解析不存在的文件"""
    parser = XMindParser()
    with pytest.raises(XMindParserError):
        parser.parse("nonexistent.xmind")


def test_parse_invalid_file():
    """测试解析无效的文件"""
    parser = XMindParser()
    # 创建一个非zip文件
    with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
        f.write(b"invalid content")
        temp_file = f.name
    
    try:
        with pytest.raises(XMindParserError):
            parser.parse(temp_file)
    finally:
        os.unlink(temp_file)


def test_parse_empty_xmind():
    """测试解析空的XMind文件"""
    parser = XMindParser()
    # 创建一个空的zip文件
    with tempfile.NamedTemporaryFile(suffix=".xmind", delete=False) as f:
        temp_file = f.name
    
    with zipfile.ZipFile(temp_file, 'w') as zf:
        pass
    
    try:
        with pytest.raises(XMindParserError):
            parser.parse(temp_file)
    finally:
        os.unlink(temp_file)