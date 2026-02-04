# XMind Converter Library

XMind Converter is a Python library for converting XMind files to and from CSV (triples), Markdown, HTML, JSON, and other file formats.

## Features

- Supports XMind file parsing
- Supports conversion to CSV, Markdown, HTML, JSON formats
- Supports conversion from CSV, Markdown, HTML, JSON formats back to XMind
- Provides command line tool
- Supports Python 3.7+

## Supported File Formats

### CSV Format
CSV files must follow a specific structure with a header row and parent-child relationships:

```csv
parent,child,relationship
Root,Child1,contains
Child1,Grandchild1,contains
Root,Child2,contains
```

### Markdown Format
Markdown files use heading levels (#, ##, ###, etc.) to represent hierarchy:

```markdown
# Root
## Child1
### Grandchild1
## Child2
```

### HTML Format
HTML files use heading tags (h1, h2, h3, etc.) to represent hierarchy:

```html
<h1>Root</h1>
<h2>Child1</h2>
<h3>Grandchild1</h3>
<h2>Child2</h2>
```

### JSON Format
JSON files must contain a specific structure with name and root_node fields:

```json
{
  "name": "MindMap Name",
  "root_node": {
    "title": "Root",
    "id": "root-id",
    "children": [
      {
        "title": "Child1",
        "id": "child1-id",
        "children": [
          {
            "title": "Grandchild1",
            "id": "grandchild1-id",
            "children": []
          }
        ]
      }
    ]
  }
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
