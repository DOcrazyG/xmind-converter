# XMind Converter

XMind Converter is a Python library for converting XMind files to and from CSV (triples), Markdown, HTML, JSON.

## Features

- Supports XMind file parsing
- Supports conversion to CSV, Markdown, HTML, JSON formats
- Supports conversion from CSV, Markdown, HTML, JSON formats back to XMind
- Provides command line tool
- Supports Python 3.7+

## Installation

### Using pip

```bash
pip install xmind-converter
```

### Install from source

```bash
# Clone repository
git clone https://github.com/yourusername/xmind-converter.git
cd xmind-converter

# Install dependencies
pip install -r requirements.txt

# Install package
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

## Testing

```bash
# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=xmind_converter
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
