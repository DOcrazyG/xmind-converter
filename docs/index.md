# XMind Converter Library

XMind Converter is a Python library for converting XMind files to and from CSV (triples), Markdown, HTML, JSON, and other file formats.

## Features

- Supports XMind file parsing (XMind 6, 7.5, and 2024+ formats)
- Supports conversion to CSV, Markdown, HTML, JSON formats
- Supports conversion from CSV, Markdown, HTML, JSON formats back to XMind
- Provides command line tool
- Supports Python 3.7+
- Full type hints for better IDE support and code quality
- Secure XML parsing using defusedxml to prevent XXE attacks
- Comprehensive test coverage (85 tests, all passing)
- Support for notes and labels in mind map nodes
- Support for detached nodes and relations between nodes

## Supported File Formats

### XMind Format
XMind files (.xmind) are ZIP archives containing either `content.json` (XMind 2024+ format) or `content.xml` (older XMind formats). The library automatically detects and handles both formats.

### CSV Format
CSV files must follow a specific structure with a header row and parent-child relationships:

```csv
parent,child,relationship
Root,Child1,contains
Child1,Grandchild1,contains
Root,Child2,contains
```

**Note**: Custom delimiters are supported via the `delimiter` parameter.

### Markdown Format
Markdown files use heading levels (#, ##, ###, etc.) to represent hierarchy. Notes and labels can be added after each node:

```markdown
# Root
- notes: Root notes
- labels: [label1, label2]

## Child1
- notes: Child notes
- labels: [label3]

### Grandchild1
## Child2
```

### HTML Format
HTML files use heading tags (h1, h2, h3, etc.) to represent hierarchy. The `<title>` tag content is used for the mind map title:

```html
<html>
<head>
    <title>MindMap Title</title>
</head>
<body>
    <h1>Root</h1>
    <h2>Child1</h2>
    <h3>Grandchild1</h3>
    <h2>Child2</h2>
</body>
</html>
```

### JSON Format
JSON files must contain a specific structure with title and topic_node fields:

```json
{
  "title": "MindMap Title",
  "topic_node": {
    "title": "Root",
    "id": "root-id",
    "notes": "Root notes",
    "labels": ["label1", "label2"],
    "children": [
      {
        "title": "Child1",
        "id": "child1-id",
        "notes": "Child notes",
        "labels": ["label3"],
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

**Note**: Only files following these specific formats can be successfully parsed and converted.

## Quick Start

### Installation

```bash
# Using uv (recommended)
# https://docs.astral.sh/uv/getting-started/installation/
curl -LsSf https://astral.sh/uv/install.sh | sh
uv add xmind-converter

# Or using pip
pip install xmind-converter
```

### Basic Usage

```python
from xmind_converter import CoreConverter

# Create converter instance
converter = CoreConverter()

# Load XMind file
mindmap = converter.load_from('example.xmind')

# Convert to CSV
converter.convert_to(mindmap, 'csv', 'output.csv')

# Convert to Markdown
converter.convert_to(mindmap, 'md', 'output.md')

# Convert to HTML
converter.convert_to(mindmap, 'html', 'output.html')

# Convert to JSON
converter.convert_to(mindmap, 'json', 'output.json')

# Convert to XMind
converter.convert_to(mindmap, 'xmind', 'output.xmind')

# Convert between formats
converter.convert('input.csv', 'output.xmind')
converter.convert('input.md', 'output.html')
```

### Command Line Usage

```bash
# Convert XMind file to CSV
xmind-converter convert example.xmind output.csv

# Convert XMind file to Markdown
xmind-converter convert example.xmind output.md

# Convert XMind file to HTML
xmind-converter convert example.xmind output.html

# Convert XMind file to JSON
xmind-converter convert example.xmind output.json

# Convert CSV to XMind
xmind-converter convert input.csv output.xmind

# Convert between any formats
xmind-converter convert input.md output.html
```

## Documentation

- [API Documentation](api.md) - Detailed API reference
- [Usage Guide](usage.md) - Comprehensive usage guide
