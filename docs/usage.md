# Usage Guide

This guide provides detailed instructions on how to use the XMind Converter library for file format conversions.

## 1. Installation

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

## 2. Python API Usage

### 2.1 Basic Conversion

#### Converting from XMind to other formats

```python
from xmind_converter import CoreConverter

# Create converter instance
converter = CoreConverter()

# Load XMind file
mindmap = converter.load_from('example.xmind')

# Convert to CSV (triples)
converter.convert_to(mindmap, 'csv', 'output.csv')

# Convert to Markdown
converter.convert_to(mindmap, 'md', 'output.md')

# Convert to HTML
converter.convert_to(mindmap, 'html', 'output.html')

# Convert to JSON
converter.convert_to(mindmap, 'json', 'output.json')
```

#### Converting from other formats to XMind

```python
from xmind_converter import CoreConverter

# Create converter instance
converter = CoreConverter()

# Convert from CSV to XMind
converter.convert('input.csv', 'output.xmind')

# Convert from Markdown to XMind
converter.convert('input.md', 'output.xmind')

# Convert from HTML to XMind
converter.convert('input.html', 'output.xmind')

# Convert from JSON to XMind
converter.convert('input.json', 'output.xmind')
```

#### Converting between any formats

```python
from xmind_converter import CoreConverter

# Create converter instance
converter = CoreConverter()

# Convert CSV to Markdown
converter.convert('input.csv', 'output.md')

# Convert Markdown to HTML
converter.convert('input.md', 'output.html')

# Convert HTML to JSON
converter.convert('input.html', 'output.json')

# Convert JSON to CSV
converter.convert('input.json', 'output.csv')
```

### 2.2 Loading and Converting Separately

#### Load file and convert to multiple formats

```python
from xmind_converter import CoreConverter

# Create converter instance
converter = CoreConverter()

# Load XMind file once
mindmap = converter.load_from('example.xmind')

# Convert to multiple formats
converter.convert_to(mindmap, 'csv', 'output.csv')
converter.convert_to(mindmap, 'md', 'output.md')
converter.convert_to(mindmap, 'html', 'output.html')
converter.convert_to(mindmap, 'json', 'output.json')
```

#### Load from different formats

```python
from xmind_converter import CoreConverter

# Create converter instance
converter = CoreConverter()

# Load from CSV
mindmap_from_csv = converter.load_from('input.csv')

# Load from Markdown
mindmap_from_md = converter.load_from('input.md')

# Load from HTML
mindmap_from_html = converter.load_from('input.html')

# Load from JSON
mindmap_from_json = converter.load_from('input.json')

# Load from XMind
mindmap_from_xmind = converter.load_from('input.xmind')
```

### 2.3 Specifying Format Explicitly

If the file extension cannot be automatically detected, you can specify the format explicitly:

```python
from xmind_converter import CoreConverter

# Create converter instance
converter = CoreConverter()

# Load with explicit format
mindmap = converter.load_from('input.txt', format_type='csv')

# Convert with explicit format
converter.convert('input.txt', 'output.txt', input_format='csv', output_format='md')
```

## 3. Command Line Tool Usage

### 3.1 Basic Commands

#### Convert XMind file

```bash
# Basic usage
xmind-converter convert <input.xmind> <output.file>

# Example: Convert to CSV
xmind-converter convert example.xmind output.csv

# Example: Convert to Markdown
xmind-converter convert example.xmind output.md

# Example: Convert to HTML
xmind-converter convert example.xmind output.html

# Example: Convert to JSON
xmind-converter convert example.xmind output.json
```

#### Convert to XMind

```bash
# Example: Convert from CSV
xmind-converter convert input.csv output.xmind

# Example: Convert from Markdown
xmind-converter convert input.md output.xmind

# Example: Convert from HTML
xmind-converter convert input.html output.xmind

# Example: Convert from JSON
xmind-converter convert input.json output.xmind
```

#### Convert between any formats

```bash
# CSV to Markdown
xmind-converter convert input.csv output.md

# Markdown to HTML
xmind-converter convert input.md output.html

# HTML to JSON
xmind-converter convert input.html output.json

# JSON to CSV
xmind-converter convert input.json output.csv
```

### 3.2 Specifying Format Explicitly

If the file extension cannot be automatically recognized, use the `--input-format` and `--output-format` options:

```bash
xmind-converter convert input.txt output.txt --input-format csv --output-format md
```

#### Available formats

- `xmind` - XMind file format
- `csv` - CSV (triples) format
- `md` - Markdown format
- `html` - HTML format
- `json` - JSON format

### 3.3 Viewing Version Information

```bash
xmind-converter info
```

### 3.4 Getting Help

```bash
# View main help
xmind-converter --help

# View convert command help
xmind-converter convert --help

# View info command help
xmind-converter info --help
```

## 4. Advanced Features

### 4.1 Working with MindMap Objects

#### Accessing MindMap structure

```python
from xmind_converter import CoreConverter

# Load XMind file
converter = CoreConverter()
mindmap = converter.load_from('example.xmind')

# Access mind map name
print(mindmap.name)

# Access root node
root = mindmap.root_node
print(root.title)

# Print tree structure
mindmap.print_tree()
```

#### Working with MindNode objects

```python
from xmind_converter import CoreConverter

# Load XMind file
converter = CoreConverter()
mindmap = converter.load_from('example.xmind')

# Access root node
root = mindmap.root_node

# Get node depth
depth = root.get_depth()
print(f"Root node depth: {depth}")

# Access children
for child in root.children:
    print(f"Child: {child.title}")
    print(f"Child depth: {child.get_depth()}")

# Add new child
from xmind_converter.models import MindNode
new_child = MindNode("New Node")
root.add_child(new_child)
```

### 4.2 Error Handling

Handle errors gracefully using try-except blocks:

```python
from xmind_converter import CoreConverter
from xmind_converter.exceptions import XMindConverterError

try:
    converter = CoreConverter()
    mindmap = converter.load_from('example.xmind')
    converter.convert_to(mindmap, 'csv', 'output.csv')
except XMindConverterError as e:
    print(f"Error: {str(e)}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

### 4.3 Batch Processing

Process multiple files in a loop:

```python
from xmind_converter import CoreConverter
import os

# Create converter instance
converter = CoreConverter()

# Process all XMind files in a directory
input_dir = 'input_xmind'
output_dir = 'output_csv'

for filename in os.listdir(input_dir):
    if filename.endswith('.xmind'):
        input_path = os.path.join(input_dir, filename)
        output_filename = filename.replace('.xmind', '.csv')
        output_path = os.path.join(output_dir, output_filename)

        try:
            converter.convert(input_path, output_path)
            print(f"Converted: {filename} -> {output_filename}")
        except Exception as e:
            print(f"Failed to convert {filename}: {str(e)}")
```

## 5. Common Questions

### 5.1 Supported XMind Versions

This library supports XMind 8 and above file formats, including:
- XMind 2024+ (JSON format)
- XMind 7.5 (XML format)
- XMind 6 (XML format)

### 5.2 Handling Large XMind Files

For large XMind files, parsing may consume significant memory. Recommendations:
- Use 64-bit Python
- Ensure sufficient available memory
- Consider processing files individually rather than in batches

### 5.3 Conversion Precision

Different file formats have different expressive capabilities, so some information may be lost during conversion:
- **CSV format**: Only preserves parent-child relationships
- **Markdown format**: Preserves hierarchy structure and titles
- **HTML format**: Adds styling information
- **JSON format**: Preserves complete structure and attributes
- **XMind format**: Preserves all information

### 5.4 File Format Detection

The library automatically detects file formats based on file extensions:
- `.xmind` - XMind format
- `.csv` - CSV format
- `.md` - Markdown format
- `.html` - HTML format
- `.json` - JSON format

If your files use non-standard extensions, specify the format explicitly using the `format_type` parameter or `--input-format`/`--output-format` options.

### 5.5 CSV Format Structure

The CSV format uses a triple structure (parent, child, relationship):

```csv
parent,child,relationship
Root,Child1,contains
Child1,Grandchild1,contains
Root,Child2,contains
```

This structure represents the hierarchical relationships in the mind map.

### 5.6 Markdown Format Structure

The Markdown format uses heading levels to represent hierarchy:

```markdown
# Root
## Child1
### Grandchild1
## Child2
```

Each heading level represents a depth level in the mind map.

### 5.7 HTML Format Structure

The HTML format generates a nested list structure:

```html
<ul>
  <li>Root
    <ul>
      <li>Child1
        <ul>
          <li>Grandchild1</li>
        </ul>
      </li>
      <li>Child2</li>
    </ul>
  </li>
</ul>
```

### 5.8 JSON Format Structure

The JSON format preserves the complete tree structure:

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

## 6. Best Practices

1. **Always validate input files** before conversion to ensure they are in the expected format
2. **Use explicit format specification** when working with non-standard file extensions
3. **Handle errors gracefully** using try-except blocks
4. **Test conversions** with sample files before processing large batches
5. **Backup original files** before performing conversions
6. **Use appropriate formats** for your use case:
   - CSV for simple parent-child relationships
   - Markdown for documentation
   - HTML for web display
   - JSON for programmatic processing
   - XMind for full feature support
