# Usage Guide

This guide provides detailed instructions on how to use the XMind Converter library for file format conversions.

## Supported File Formats

**Important**: This library only supports files following specific formats. Files not conforming to these formats will fail to parse.

### CSV Format

CSV files must follow a specific structure:
- **Header row**: Required, with columns `parent,child,relationship`
- **Data rows**: Each row defines a parent-child relationship
- **Delimiter**: Default is comma (`,`), but can be customized

**Example CSV file**:
```csv
parent,child,relationship
Root,Child1,contains
Child1,Grandchild1,contains
Child1,Grandchild2,contains
Root,Child2,contains
Child2,Grandchild3,contains
```

**Requirements**:
- Must have a header row
- Each row must have at least 2 columns (parent, child)
- The third column (relationship) is ignored during parsing
- The first parent node in the file becomes the root node

### Markdown Format

Markdown files use heading levels to represent hierarchy:
- **# (H1)**: Root level
- **## (H2)**: First level children
- **### (H3)**: Second level children
- And so on...

**Example Markdown file**:
```markdown
# Root
## Child1
### Grandchild1
### Grandchild2
## Child2
### Grandchild3
```

**Requirements**:
- Must use heading syntax (#, ##, ###, etc.)
- Empty lines are ignored
- Heading level determines the node depth in the tree
- The first H1 heading becomes the root node

### HTML Format

HTML files use heading tags (h1, h2, h3, etc.) to represent hierarchy:
- **h1**: Root level
- **h2**: First level children
- **h3**: Second level children
- And so on...

**Example HTML file**:
```html
<h1>Root</h1>
<h2>Child1</h2>
<h3>Grandchild1</h3>
<h3>Grandchild2</h3>
<h2>Child2</h2>
<h3>Grandchild3</h3>
```

**Requirements**:
- Must use heading tags (h1, h2, h3, etc.)
- Heading level determines the node depth in the tree
- The h1 content becomes the mind map name and root node title
- Only heading tags are parsed; other HTML content is ignored

### JSON Format

JSON files must contain a specific structure with `name` and `root_node` fields:

**Example JSON file**:
```json
{
  "name": "My MindMap",
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
          },
          {
            "title": "Grandchild2",
            "id": "grandchild2-id",
            "children": []
          }
        ]
      },
      {
        "title": "Child2",
        "id": "child2-id",
        "children": [
          {
            "title": "Grandchild3",
            "id": "grandchild3-id",
            "children": []
          }
        ]
      }
    ]
  }
}
```

**Requirements**:
- Must have a `name` field (string) for the mind map name
- Must have a `root_node` field (object) representing the root node
- Each node must have:
  - `title` (string): Node title
  - `id` (string, optional): Node ID, auto-generated if not provided
  - `children` (array): Array of child node objects
- `children` array can be empty for leaf nodes

**Legacy format support**: The parser also supports a simplified format where the root object itself is the root node:
```json
{
  "title": "Root",
  "id": "root-id",
  "children": [...]
}
```

## 1. Installation

### Using uv (Recommended)

```bash
# Using uv (recommended)
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

# Get mind map depth (method)
depth = mindmap.get_depth()
print(f"Mind map depth: {depth}")

# Get mind map depth (property)
depth = mindmap.depth
print(f"Mind map depth: {depth}")

# Print tree structure
mindmap.print_tree()

# Traverse mind map
def print_node(node, depth):
    print(f"{'  ' * depth}{node.title}")

mindmap.traverse(print_node)

# Add root node
from xmind_converter.models import MindNode
new_root = MindNode("New Root")
mindmap.add_root_node(new_root)
```

#### Working with MindNode objects

```python
from xmind_converter import CoreConverter

# Load XMind file
converter = CoreConverter()
mindmap = converter.load_from('example.xmind')

# Access root node
root = mindmap.root_node

# Get node depth (method)
depth = root.get_depth()
print(f"Root node depth: {depth}")

# Get node depth (property)
depth = root.depth
print(f"Root node depth: {depth}")

# Access children
for child in root.children:
    print(f"Child: {child.title}")
    print(f"Child depth: {child.get_depth()}")

# Add new child
from xmind_converter.models import MindNode
new_child = MindNode("New Node")
root.add_child(new_child)

# Remove child
if root.children:
    root.remove_child(root.children[0])

# Traverse node tree
def print_node(node, depth):
    print(f"{'  ' * depth}{node.title}")

root.traverse(print_node)

# Print node tree structure
root.print_tree()
```

### 4.2 Error Handling

Handle errors gracefully using try-except blocks:

```python
from xmind_converter import CoreConverter
from xmind_converter.exceptions import XMindConverterError, ParserError, ConverterError, FileFormatError

try:
    converter = CoreConverter()
    mindmap = converter.load_from('example.xmind')
    converter.convert_to(mindmap, 'csv', 'output.csv')
except ParserError as e:
    print(f"Parsing error: {str(e)}")
except ConverterError as e:
    print(f"Conversion error: {str(e)}")
except FileFormatError as e:
    print(f"File format error: {str(e)}")
except XMindConverterError as e:
    print(f"General error: {str(e)}")
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

**Note**: When parsing CSV files, the third column (relationship) is ignored. Only the parent-child relationships are used to build the tree structure.

### 5.6 Markdown Format Structure

The Markdown format uses heading levels to represent hierarchy:

```markdown
# Root
## Child1
### Grandchild1
## Child2
```

Each heading level represents a depth level in the mind map.

**Note**: When parsing Markdown files, only lines starting with # are processed. Empty lines and other content are ignored.

### 5.7 HTML Format Structure

**Output Format**: When converting to HTML, the library generates a nested list structure:

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

**Input Format**: When parsing HTML files, only heading tags (h1, h2, h3, etc.) are processed. The heading level determines the node depth. Other HTML content is ignored.

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

**Note**: When parsing JSON files, the library supports two formats:
1. Standard format with `name` and `root_node` fields
2. Legacy format where the root object itself is the root node (must have `title` and `children` fields)

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
