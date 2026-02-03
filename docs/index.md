# XMind Converter Library

XMind Converter is a Python library for converting XMind files to and from CSV (triples), Markdown, HTML, JSON, and other file formats.

## Features

- Supports XMind file parsing
- Supports conversion to CSV, Markdown, HTML, JSON formats
- Supports conversion from CSV, Markdown, JSON formats back to XMind (partial support)
- Provides command line tool
- Supports Python 3.7+

## Quick Start

### Installation

```bash
pip install xmind-converter
```

### Basic Usage

```python
from xmind_converter import XMindConverter

# Create converter instance
converter = XMindConverter()

# Load XMind file
node = converter.load_xmind('example.xmind')

# Convert to CSV
csv_content = converter.convert_to(node, 'csv')
print(csv_content)

# Convert to Markdown
md_content = converter.convert_to(node, 'md')
print(md_content)

# Convert to HTML
html_content = converter.convert_to(node, 'html')
print(html_content)

# Convert to JSON
json_content = converter.convert_to(node, 'json')
print(json_content)
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
```