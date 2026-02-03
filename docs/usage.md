# 使用指南

本指南将详细介绍如何使用XMind转换器库进行文件格式转换。

## 1. 安装

### 使用pip安装

```bash
pip install xmind-converter
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/xmind-converter.git
cd xmind-converter

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

## 2. Python API使用

### 2.1 基本转换

#### 从XMind转换到其他格式

```python
from xmind_converter import XMindConverter

# 创建转换器实例
converter = XMindConverter()

# 加载XMind文件
node = converter.load_xmind('example.xmind')

# 转换为CSV（三元组）
csv_content = converter.convert_to(node, 'csv')
print(csv_content)

# 转换为Markdown
md_content = converter.convert_to(node, 'md')
print(md_content)

# 转换为HTML
html_content = converter.convert_to(node, 'html')
print(html_content)

# 转换为JSON
json_content = converter.convert_to(node, 'json')
print(json_content)
```

#### 保存到文件

```python
# 转换并保存到文件
converter.convert_to(node, 'csv', 'output.csv')
converter.convert_to(node, 'md', 'output.md')
converter.convert_to(node, 'html', 'output.html')
converter.convert_to(node, 'json', 'output.json')
```

### 2.2 反向转换

#### 从其他格式转换到XMind

```python
from xmind_converter import XMindConverter

# 创建转换器实例
converter = XMindConverter()

# 从CSV转换
node_from_csv = converter.convert_from('input.csv', 'csv')

# 从Markdown转换
node_from_md = converter.convert_from('input.md', 'md')

# 从JSON转换
node_from_json = converter.convert_from('input.json', 'json')

# 注意：HTML反向转换暂未实现
```

## 3. 命令行工具使用

### 3.1 基本命令

#### 转换XMind文件

```bash
# 基本用法
xmind-converter convert <input.xmind> <output.file>

# 示例：转换为CSV
xmind-converter convert example.xmind output.csv

# 示例：转换为Markdown
xmind-converter convert example.xmind output.md

# 示例：转换为HTML
xmind-converter convert example.xmind output.html

# 示例：转换为JSON
xmind-converter convert example.xmind output.json
```

#### 指定格式

如果输出文件名的扩展名不能自动识别格式，可以使用`--format`选项指定：

```bash
xmind-converter convert example.xmind output.txt --format csv
```

#### 反向转换

```bash
# 基本用法
xmind-converter reverse <input.file> <output.xmind>

# 示例：从CSV转换
xmind-converter reverse input.csv output.xmind

# 示例：从Markdown转换
xmind-converter reverse input.md output.xmind

# 示例：从JSON转换
xmind-converter reverse input.json output.xmind
```

#### 查看版本信息

```bash
xmind-converter info
```

## 4. 高级功能

### 4.1 自定义CSV分隔符

```python
from xmind_converter import XMindConverter

converter = XMindConverter()
node = converter.load_xmind('example.xmind')

# 使用分号作为分隔符
csv_content = converter.convert_to(node, 'csv', delimiter=';')
print(csv_content)
```

### 4.2 处理节点属性

XMind节点可能包含各种属性，这些属性会在转换时被保留：

```python
from xmind_converter import Node

# 创建带有属性的节点
node = Node(
    "测试节点",
    attributes={"color": "red", "priority": "high"}
)

# 转换为JSON时会包含属性
from xmind_converter import XMindConverter
converter = XMindConverter()
json_content = converter.convert_to(node, 'json')
print(json_content)
```

## 5. 常见问题

### 5.1 支持的XMind版本

本库支持XMind 8及以上版本的文件格式。

### 5.2 处理大型XMind文件

对于大型XMind文件，解析可能会消耗较多内存。建议在处理大型文件时使用64位Python，并确保有足够的内存。

### 5.3 转换精度

由于不同文件格式的表达能力不同，转换过程中可能会丢失一些信息，例如：
- CSV格式只能保留父子关系
- Markdown格式只能保留层级结构和标题
- HTML格式会添加一些样式信息
- JSON格式可以保留完整的结构和属性

### 5.4 错误处理

在使用过程中，如果遇到错误，可以捕获`XMindConverterError`异常：

```python
from xmind_converter import XMindConverter, XMindConverterError

try:
    converter = XMindConverter()
    node = converter.load_xmind('example.xmind')
except XMindConverterError as e:
    print(f"错误: {str(e)}")
```