# XMind Converter

XMind Converter is a Python library for converting XMind files to and from CSV (triples), Markdown, HTML, JSON.

## Features

- Supports XMind file parsing
- Supports conversion to CSV, Markdown, HTML, JSON formats
- Supports conversion from CSV, Markdown, HTML, JSON formats back to XMind
- Provides command line tool
- Supports Python 3.7+
- Full type hints for better IDE support and code quality
- Secure XML parsing using defusedxml to prevent XXE attacks
- Comprehensive test coverage

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

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
# https://docs.astral.sh/uv/getting-started/installation/
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install xmind-converter
uv add xmind-converter
```

### Using pip

```bash
pip install xmind-converter
```

### Install from source

```bash
# Clone repository
git clone https://github.com/DOcrazyG/xmind-converter.git
cd xmind-converter

# Install using uv (recommended)
uv add .

# Or using pip
pip install -e .
```

## Basic Usage

### Python API

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

# Convert from CSV to XMind
converter.convert('input.csv', 'output.xmind')

# Convert from Markdown to XMind
converter.convert('input.md', 'output.xmind')

# Convert from HTML to XMind
converter.convert('input.html', 'output.xmind')

# Convert from JSON to XMind
converter.convert('input.json', 'output.xmind')
```

### Command Line Tool

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

# Convert Markdown to XMind
xmind-converter convert input.md output.xmind

# Convert HTML to XMind
xmind-converter convert input.html output.xmind

# Convert JSON to XMind
xmind-converter convert input.json output.xmind

# Convert between any formats
xmind-converter convert input.csv output.md

# View version information
xmind-converter info
```

## Project Structure

```
xmind_converter/
├── __init__.py          # Package initialization
├── core.py              # Core converter class
├── models.py            # Data models (MindMap, MindNode)
├── parsers/             # Parser modules
│   ├── __init__.py
│   ├── base_parser.py   # Base parser class
│   ├── xmind_parser.py  # XMind file parser
│   ├── csv_parser.py    # CSV parser
│   ├── md_parser.py     # Markdown parser
│   ├── html_parser.py   # HTML parser
│   └── json_parser.py   # JSON parser
├── converters/          # Converter modules
│   ├── __init__.py
│   ├── base_converter.py   # Base converter class
│   ├── csv_converter.py    # CSV converter
│   ├── md_converter.py     # Markdown converter
│   ├── html_converter.py   # HTML converter
│   ├── json_converter.py   # JSON converter
│   └── xmind_converter.py  # XMind converter
├── exceptions.py        # Exception definitions
└── cli.py               # Command line tool
tests/                   # Test code
docs/                    # Documentation
```

## Dependencies

- Python 3.7+
- click >= 8.0.0
- defusedxml >= 0.7.1 (for secure XML parsing)

### Development Dependencies

- pytest >= 7.4.4 (testing)
- black >= 23.3.0 (code formatting)
- flake8 >= 5.0.4 (linting)
- mypy >= 1.0.0 (type checking)

## Testing

```bash
# Run tests using uv (recommended)
uv run pytest tests/

# Run tests with coverage
uv run pytest tests/ --cov=xmind_converter

# Or using pip
pytest tests/
pytest tests/ --cov=xmind_converter
```

## Development

```bash
# Install development dependencies using uv
uv add --dev .

# Or using pip
pip install -e ".[dev]"

# Format code with black
uv run black xmind_converter/ tests/

# Or using pip
black xmind_converter/ tests/

# Lint code with flake8
uv run flake8 xmind_converter/ tests/

# Or using pip
flake8 xmind_converter/ tests/
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Contact

- Author: DOcrazyG
- Email: lyuuhao@gmail.com
- Project Link: https://github.com/DOcrazyG/xmind-converter.git
