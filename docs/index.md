# XMind Converter Library

XMind Converter is a Python library for converting XMind files to and from CSV (triples), Markdown, HTML, JSON, and other file formats.

## Features

- Supports XMind file parsing
- Supports conversion to CSV, Markdown, HTML, JSON formats
- Supports conversion from CSV, Markdown, HTML, JSON formats back to XMind
- Provides command line tool
- Supports Python 3.7+

## Quick Start

### Installation

```bash
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
