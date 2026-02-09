# XMind Converter

[English](README.md) | 简体中文

XMind Converter 是一个用于在 XMind 文件与 CSV（三元组）、Markdown、HTML、JSON 等格式之间进行转换的 Python 库。其中，CSV、HTML格式只保留主题节点的文本信息，Markdown在此基础上还保留了备注（notes）和标签（labels）的信息，JSON格式则保留了主题节点、自由节点和关系的全部文本信息。

## 功能特性

- 支持 XMind 文件解析（XMind 6、7.5 和 2024+ 格式）
- 支持转换为 CSV、Markdown、HTML、JSON 和 XMind 格式
- 支持从 CSV、Markdown、HTML、JSON 格式转换回 XMind
- 提供命令行工具
- 支持 Python 3.7+
- 完整的类型提示，提供更好的 IDE 支持和代码质量
- 使用 defusedxml 进行安全的 XML 解析，防止 XXE 攻击
- 全面的测试覆盖
- 支持节点备注和标签提取
- 支持自由节点和关系
- 支持 XMind 来回转换

## 支持的文件格式

### CSV 格式
CSV 文件必须遵循特定的文件格式，包含标题行和具体三元组：

```csv
parent,child,relationship
Root,Child1,contains
Child1,Grandchild1,contains
Root,Child2,contains
```

### Markdown 格式
Markdown 文件使用标题级别（#、##、### 等）来表示层级关系：

```markdown
# Root
## Child1
### Grandchild1
## Child2
```

**备注和标签支持**：
Markdown 文件可以为每个节点包含备注和标签：

```markdown
# Root
- notes: 这是根节点的备注
- labels: [标签1, 标签2]

## Child1
- notes: 这是子节点 1 的备注
- labels: [子标签]
```

### HTML 格式
HTML 文件使用标题标签（h1、h2、h3 等）来表示层级关系：

```html
<h1>Root</h1>
<h2>Child1</h2>
<h3>Grandchild1</h3>
<h2>Child2</h2>
```

**标题标签支持**：
HTML 解析器从 HTML 头部分的 `<title>` 标签中提取思维导图名称。

### JSON 格式
JSON 文件必须包含特定的结构，包含 title 和 topic_node 字段：

```json
{
  "title": "思维导图名称",
  "topic_node": {
    "title": "Root",
    "id": "root-id",
    "notes": "节点的可选备注",
    "labels": ["标签1", "标签2"],
    "children": [
      {
        "title": "Child1",
        "id": "child1-id",
        "notes": "可选备注",
        "labels": ["子标签"],
        "children": [
          {
            "title": "Grandchild1",
            "id": "grandchild1-id",
            "children": []
          }
        ]
      }
    ]
  },
  "detached_nodes": [],
  "relations": []
}
```

**自由节点**：不在结构化树中的自由主题节点。

**关系**：节点之间的关系，包含 source_id、target_id 和 title。

**注意**：解析器还支持带有 `name` 和 `root_node` 字段的旧格式，以保持向后兼容性。

## 安装

### 使用 uv（推荐）

```bash
# 如果尚未安装 uv，请先安装
# https://docs.astral.sh/uv/getting-started/installation/
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 xmind-converter
uv add xmind-converter
```

### 使用 pip

```bash
pip install xmind-converter
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/DOcrazyG/xmind-converter.git
cd xmind-converter

# 使用 uv 安装（推荐）
uv add .

# 或使用 pip
pip install -e .
```

## 基本用法

### Python API

```python
from xmind_converter import CoreConverter

# 创建转换器实例
converter = CoreConverter()

# 加载 XMind 文件
mindmap = converter.load_from('example.xmind')

# 转换为 CSV
converter.convert_to(mindmap, 'csv', 'output.csv')

# 转换为 Markdown
converter.convert_to(mindmap, 'md', 'output.md')

# 转换为 HTML
converter.convert_to(mindmap, 'html', 'output.html')

# 转换为 JSON
converter.convert_to(mindmap, 'json', 'output.json')

# 从 CSV 转换为 XMind
converter.convert('input.csv', 'output.xmind')

# 从 Markdown 转换为 XMind
converter.convert('input.md', 'output.xmind')

# 从 HTML 转换为 XMind
converter.convert('input.html', 'output.xmind')

# 从 JSON 转换为 XMind
converter.convert('input.json', 'output.xmind')
```

### 命令行工具

```bash
# 将 XMind 文件转换为 CSV
xmind-converter convert example.xmind output.csv

# 将 XMind 文件转换为 Markdown
xmind-converter convert example.xmind output.md

# 将 XMind 文件转换为 HTML
xmind-converter convert example.xmind output.html

# 将 XMind 文件转换为 JSON
xmind-converter convert example.xmind output.json

# 将 CSV 转换为 XMind
xmind-converter convert input.csv output.xmind

# 将 Markdown 转换为 XMind
xmind-converter convert input.md output.xmind

# 将 HTML 转换为 XMind
xmind-converter convert input.html output.xmind

# 将 JSON 转换为 XMind
xmind-converter convert input.json output.xmind

# 在任意格式之间转换
xmind-converter convert input.csv output.md

# 查看版本信息
xmind-converter info
```

## 项目结构

```
xmind_converter/
├── __init__.py          # 包初始化
├── core.py              # 核心转换器类
├── models.py            # 数据模型（MindMap、Node）
├── parsers/             # 解析器模块
│   ├── __init__.py
│   ├── base_parser.py   # 基础解析器类
│   ├── xmind_parser.py  # XMind 文件解析器
│   ├── csv_parser.py    # CSV 解析器
│   ├── md_parser.py     # Markdown 解析器
│   ├── html_parser.py   # HTML 解析器
│   └── json_parser.py   # JSON 解析器
├── converters/          # 转换器模块
│   ├── __init__.py
│   ├── base_converter.py   # 基础转换器类
│   ├── csv_converter.py    # CSV 转换器
│   ├── md_converter.py     # Markdown 转换器
│   ├── html_converter.py   # HTML 转换器
│   ├── json_converter.py   # JSON 转换器
│   └── xmind_converter.py  # XMind 转换器
├── exceptions.py        # 异常定义
└── cli.py               # 命令行工具
tests/                   # 测试代码
docs/                    # 文档
```

## 依赖项

- Python 3.7+
- click >= 8.0.0
- defusedxml >= 0.7.1（用于安全的 XML 解析）

### 开发依赖

- pytest >= 7.4.4（测试）
- black >= 23.3.0（代码格式化）
- flake8 >= 5.0.4（代码检查）
- mypy >= 1.0.0（类型检查）

## 测试

```bash
# 使用 uv 运行测试（推荐）
uv run pytest tests/

# 运行测试并生成覆盖率报告
uv run pytest tests/ --cov=xmind_converter

# 或使用 pip
pytest tests/
pytest tests/ --cov=xmind_converter
```

## 开发

```bash
# 使用 uv 安装开发依赖
uv add --dev .

# 或使用 pip
pip install -e ".[dev]"

# 使用 black 格式化代码
uv run black xmind_converter/ tests/

# 或使用 pip
black xmind_converter/ tests/

# 使用 flake8 检查代码
uv run flake8 xmind_converter/ tests/

# 或使用 pip
flake8 xmind_converter/ tests/
```

## 贡献

欢迎贡献！请按照以下步骤操作：

1. Fork 仓库
2. 创建功能分支（`git checkout -b feature/AmazingFeature`）
3. 提交更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件

## 联系方式

- 作者：DOcrazyG
- 邮箱：lyuuhao@gmail.com
- 项目链接：https://github.com/DOcrazyG/xmind-converter.git
