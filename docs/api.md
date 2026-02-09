# API Documentation

This document provides detailed API reference for the XMind Converter library.

## Core Classes

### CoreConverter

**Description**: Main converter class, used for loading files and performing format conversions between XMind, CSV, Markdown, HTML, and JSON formats.

**Methods**:

#### `__init__()`

Initialize converter instance.

**Parameters**: None

**Return Value**: CoreConverter instance

**Type**: `CoreConverter`

#### `load_from(input_path, format_type=None, **kwargs)`

Load from specified format and convert to MindMap.

**Parameters**:
- `input_path` (str): Path to the input file
- `format_type` (str, optional): Format type (auto-detected from file extension if not provided). Supported: 'xmind', 'csv', 'md', 'html', 'json'
- `**kwargs`: Additional format-specific parameters

**Return Value**: `MindMap` object representing the parsed content

**Type**: `MindMap`

**Exceptions**:
- `ParserError`: Raised when loading fails or format is unsupported
- `FileFormatError`: Raised when file format is not supported

**Example**:
```python
converter = CoreConverter()
mindmap = converter.load_from('example.xmind')
mindmap = converter.load_from('data.csv', format_type='csv')
```

#### `convert_to(mindmap, format_type, output_path, **kwargs)`

Convert MindMap to specified format and save to file.

**Parameters**:
- `mindmap` (MindMap): MindMap object to convert
- `format_type` (str): Target format type. Supported: 'csv', 'md', 'html', 'json', 'xmind'
- `output_path` (str): Path to save the output file
- `**kwargs`: Additional format-specific parameters

**Return Value**: str - Success message

**Type**: `str`

**Exceptions**:
- `ConverterError`: Raised when conversion fails or format is unsupported
- `FileFormatError`: Raised when file format is not supported

**Example**:
```python
converter = CoreConverter()
mindmap = converter.load_from('example.xmind')
result = converter.convert_to(mindmap, 'csv', 'output.csv')
```

#### `convert(input_path, output_path, input_format=None, output_format=None, **kwargs)`

Convert from one format to another.

**Parameters**:
- `input_path` (str): Path to the input file
- `output_path` (str): Path to save the output file
- `input_format` (str, optional): Input format type (auto-detected from file extension if not provided)
- `output_format` (str, optional): Output format type (auto-detected from file extension if not provided)
- `**kwargs`: Additional format-specific parameters

**Return Value**: str - Success message

**Type**: `str`

**Exceptions**:
- `ParserError`: Raised when loading fails or format is unsupported
- `ConverterError`: Raised when conversion fails or format is unsupported
- `FileFormatError`: Raised when file format is not supported

**Example**:
```python
converter = CoreConverter()
result = converter.convert('input.xmind', 'output.csv')
result = converter.convert('input.csv', 'output.xmind')
result = converter.convert('input.md', 'output.html')
```

## Data Models

### MindMap

**Description**: Mind map class representing the entire mind map structure with topic node, detached nodes, and relations.

**Methods**:

#### `__init__(title, topic_node=None, detached_nodes=None, relations=None)`

Initialize MindMap instance.

**Parameters**:
- `title` (str, optional): Mind map title, defaults to "Untitled"
- `topic_node` (TopicNode, optional): Topic node (root node) of the mind map
- `detached_nodes` (list[DetachedNode], optional): List of detached nodes
- `relations` (list[Relation], optional): List of relations between nodes

**Return Value**: MindMap instance

#### `__str__()`

Get string representation of the mind map.

**Parameters**: None

**Return Value**: str - String representation

#### `__repr__()`

Get detailed string representation of the mind map.

**Parameters**: None

**Return Value**: str - Detailed string representation

#### `get_depth()`

Get mind map depth (maximum depth of the entire tree).

**Parameters**: None

**Return Value**: int - Mind map depth

#### `depth`

Property to get mind map depth (maximum depth of the entire tree).

**Return Value**: int - Mind map depth

#### `traverse(callback)`

Traverse mind map and execute callback for each node.

**Parameters**:
- `callback` (function): Callback function that receives (node, depth) as parameters

**Return Value**: None

#### `add_detached_node(node)`

Add detached node to mind map.

**Parameters**:
- `node` (DetachedNode): Detached node object

**Return Value**: None

#### `remove_detached_node(node)`

Remove detached node from mind map.

**Parameters**:
- `node` (DetachedNode): Detached node object to remove

**Return Value**: None

#### `add_relation(relation)`

Add relation to mind map.

**Parameters**:
- `relation` (Relation): Relation object

**Return Value**: None

#### `remove_relation(relation)`

Remove relation from mind map.

**Parameters**:
- `relation` (Relation): Relation object to remove

**Return Value**: None

#### `get_node_by_id(node_id)`

Get node by ID from mind map (searches topic node and detached nodes).

**Parameters**:
- `node_id` (str): Node ID to search for

**Return Value**: Node or None - Node object if found, None otherwise

#### `print_tree()`

Print mind map tree structure to console, including notes and labels.

**Parameters**: None

**Return Value**: None

### Node

**Description**: Base node class for mind map nodes, representing a generic node with title, children, notes, and labels.

**Methods**:

#### `__init__(title, node_id=None, children=None, notes=None, labels=None)`

Initialize node instance.

**Parameters**:
- `title` (str): Node title
- `node_id` (str, optional): Node ID, auto-generated if not provided
- `children` (list[Node], optional): Child node list
- `notes` (str, optional): Node notes
- `labels` (list[str], optional): Node labels

**Return Value**: Node instance

#### `add_child(child)`

Add child node.

**Parameters**:
- `child` (Node): Child node object

**Return Value**: None

#### `remove_child(child)`

Remove child node.

**Parameters**:
- `child` (Node): Child node object to remove

**Return Value**: None

#### `add_label(label)`

Add label to node.

**Parameters**:
- `label` (str): Label to add

**Return Value**: None

#### `remove_label(label)`

Remove label from node.

**Parameters**:
- `label` (str): Label to remove

**Return Value**: None

#### `get_depth()`

Get node depth.

**Parameters**: None

**Return Value**: int - Node depth

#### `depth`

Property to get node depth.

**Return Value**: int - Node depth

#### `traverse(callback, depth=None)`

Traverse node tree and execute callback for each node.

**Parameters**:
- `callback` (function): Callback function that receives (node, depth) as parameters
- `depth` (int, optional): Starting depth level

**Return Value**: None

#### `__str__()`

Get string representation of the node, including notes and labels.

**Parameters**: None

**Return Value**: str - String representation

#### `__repr__()`

Get detailed string representation of the node, including notes and labels.

**Parameters**: None

**Return Value**: str - Detailed string representation

#### `print_tree(indent=0, prefix="")`

Print node tree structure to console, including notes and labels.

**Parameters**:
- `indent` (int, optional): Indentation level
- `prefix` (str, optional): Prefix string for display

**Return Value**: None

### TopicNode

**Description**: Topic node class representing the root node of the mind map structure. Inherits from Node.

**Methods**:

#### `__init__(title, node_id=None, children=None, notes=None, labels=None)`

Initialize topic node instance.

**Parameters**:
- `title` (str): Node title
- `node_id` (str, optional): Node ID, auto-generated if not provided
- `children` (list[Node], optional): Child node list
- `notes` (str, optional): Node notes
- `labels` (list[str], optional): Node labels

**Return Value**: TopicNode instance

#### `get_depth()`

Get topic node depth (always 0 for root node).

**Parameters**: None

**Return Value**: int - Topic node depth (0)

#### `depth`

Property to get topic node depth (always 0 for root node).

**Return Value**: int - Topic node depth (0)

#### `traverse(callback, depth=0)`

Traverse topic node tree and execute callback for each node.

**Parameters**:
- `callback` (function): Callback function that receives (node, depth) as parameters
- `depth` (int, optional): Starting depth level (default: 0)

**Return Value**: None

### DetachedNode

**Description**: Detached node class representing free-standing nodes that are not part of the main topic tree. Inherits from Node.

**Methods**:

#### `__init__(title, node_id=None, children=None, notes=None, labels=None)`

Initialize detached node instance.

**Parameters**:
- `title` (str): Node title
- `node_id` (str, optional): Node ID, auto-generated if not provided
- `children` (list[Node], optional): Child node list
- `notes` (str, optional): Node notes
- `labels` (list[str], optional): Node labels

**Return Value**: DetachedNode instance

### Relation

**Description**: Relation class representing relationships between nodes in the mind map.

**Methods**:

#### `__init__(source_id, target_id, relation_id=None, title="Relation")`

Initialize relation instance.

**Parameters**:
- `source_id` (str): Source node ID
- `target_id` (str): Target node ID
- `relation_id` (str, optional): Relation ID, auto-generated if not provided
- `title` (str, optional): Relation title, defaults to "Relation"

**Return Value**: Relation instance

## Converter Classes

### BaseConverter

**Description**: Abstract base class for all converters.

**Methods**:

#### `convert_to(mindmap, output_path, **kwargs)`

Convert MindMap to specified format (abstract method).

**Parameters**:
- `mindmap` (MindMap): MindMap object to convert
- `output_path` (str): Path to save the output file
- `**kwargs`: Additional format-specific parameters

**Return Value**: None

**Exceptions**:
- `NotImplementedError`: Must be implemented by subclasses

### CSVConverter

**Description**: CSV format converter.

**Methods**:

#### `convert_to(mindmap, output_path, **kwargs)`

Convert MindMap to CSV format and save to file.

**Parameters**:
- `mindmap` (MindMap): MindMap object to convert
- `output_path` (str): Path to save the CSV file
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: None

### MarkdownConverter

**Description**: Markdown format converter.

**Methods**:

#### `convert_to(mindmap, output_path, **kwargs)`

Convert MindMap to Markdown format and save to file. Includes notes and labels for each node.

**Parameters**:
- `mindmap` (MindMap): MindMap object to convert
- `output_path` (str): Path to save the Markdown file
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: None

**Output Format**:
```markdown
# Root Title
- notes: Root notes
- labels: [label1, label2]

## Child Title
- notes: Child notes
- labels: [label3]

### Grandchild Title
```

### HTMLConverter

**Description**: HTML format converter.

**Methods**:

#### `convert_to(mindmap, output_path, **kwargs)`

Convert MindMap to HTML format and save to file.

**Parameters**:
- `mindmap` (MindMap): MindMap object to convert
- `output_path` (str): Path to save the HTML file
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: None

### JSONConverter

**Description**: JSON format converter.

**Methods**:

#### `convert_to(mindmap, output_path, **kwargs)`

Convert MindMap to JSON format and save to file. Includes notes, labels, detached nodes, and relations.

**Parameters**:
- `mindmap` (MindMap): MindMap object to convert
- `output_path` (str): Path to save the JSON file
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: None

**Output Format**:
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
        "children": []
      }
    ]
  },
  "detached_nodes": [],
  "relations": []
}
```

### XMindConverter

**Description**: XMind file format converter.

**Methods**:

#### `convert_to(mindmap, output_path, **kwargs)`

Convert MindMap to XMind file format and save to file.

**Parameters**:
- `mindmap` (MindMap): MindMap object to convert
- `output_path` (str): Path to save the XMind file
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: None

## Parser Classes

### BaseParser

**Description**: Abstract base class for all parsers.

**Methods**:

#### `parse(input_path, **kwargs)`

Parse file and return MindMap (abstract method).

**Parameters**:
- `input_path` (str): Path to the input file
- `**kwargs`: Additional format-specific parameters

**Return Value**: MindMap

**Exceptions**:
- `NotImplementedError`: Must be implemented by subclasses

### XMindParser

**Description**: XMind file parser.

**Supported Format**: XMind files (.xmind) are ZIP archives containing either `content.json` (XMind 2024+ format) or `content.xml` (older XMind formats). The parser automatically detects and handles both formats, including XMind 6, 7.5, and 2024+ versions.

**Security**: The parser uses `defusedxml` library when parsing XML-based XMind files to prevent XXE (XML External Entity) attacks. This provides protection against external entity expansion, parameter entity attacks, and external DTD retrieval.

**Format Requirements**:
- File must be a valid ZIP archive
- Must contain either `content.json` or `content.xml`
- `content.json` format: Array of sheet objects or object with "sheets" key
- `content.xml` format: XML with proper namespace `urn:xmind:xmap:xmlns:content:2.0`
- Must contain at least one sheet with a root topic

**Methods**:

#### `parse(input_path, **kwargs)`

Parse XMind file.

**Parameters**:
- `input_path` (str): XMind file path
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: MindMap object representing the parsed content

**Exceptions**:
- `ParserError`: Raised when parsing fails
- `FileNotFoundError`: Raised when file is not found
- `FileFormatError`: Raised when file is not a valid XMind file

### CSVParser

**Description**: CSV file parser.

**Supported Format**: CSV files must have a header row with columns `parent,child,relationship`. Each data row defines a parent-child relationship. The third column (relationship) is ignored during parsing.

**Example CSV format**:
```csv
parent,child,relationship
Root,Child1,contains
Child1,Grandchild1,contains
```

**Methods**:

#### `parse(input_path, **kwargs)`

Parse CSV file.

**Parameters**:
- `input_path` (str): CSV file path
- `delimiter` (str, optional): CSV delimiter character (default: ",")
- `**kwargs`: Additional parameters

**Return Value**: MindMap object representing the parsed content

**Exceptions**:
- `ParserError`: Raised when parsing fails
- `FileNotFoundError`: Raised when file is not found

### MarkdownParser

**Description**: Markdown file parser.

**Supported Format**: Markdown files must use heading syntax (#, ##, ###, etc.) to represent hierarchy. Heading level determines node depth. Notes and labels can be added after each node using the format `- notes:XXX` and `- labels:[label1, label2]`.

**Example Markdown format**:
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

**Methods**:

#### `parse(input_path, **kwargs)`

Parse Markdown file.

**Parameters**:
- `input_path` (str): Markdown file path
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: MindMap object representing the parsed content

**Exceptions**:
- `ParserError`: Raised when parsing fails
- `FileNotFoundError`: Raised when file is not found

### HTMLParser

**Description**: HTML file parser.

**Supported Format**: HTML files must use heading tags (h1, h2, h3, etc.) to represent hierarchy. Heading level determines node depth. The h1 content becomes the mind map title and root node title. The `<title>` tag content is used for the mind map title if present. Only heading tags are parsed; other HTML content is ignored.

**Example HTML format**:
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

**Methods**:

#### `parse(input_path, **kwargs)`

Parse HTML file.

**Parameters**:
- `input_path` (str): HTML file path
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: MindMap object representing the parsed content

**Exceptions**:
- `ParserError`: Raised when parsing fails
- `FileNotFoundError`: Raised when file is not found

### JSONParser

**Description**: JSON file parser.

**Supported Format**: JSON files must contain a specific structure. Two formats are supported:

**Standard format** (recommended):
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
        "children": []
      }
    ]
  },
  "detached_nodes": [],
  "relations": []
}
```

**Legacy format** (for compatibility):
```json
{
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
      "children": []
    }
  ]
}
```

**Requirements**:
- Standard format: Must have `title` (string) and `topic_node` (object) fields, optional `detached_nodes` and `relations` fields
- Legacy format: Root object must have `title` and `children` fields
- Each node must have:
  - `title` (string): Node title
  - `id` (string, optional): Node ID, auto-generated if not provided
  - `notes` (string, optional): Node notes
  - `labels` (array of string, optional): Node labels
  - `children` (array): Array of child node objects

**Methods**:

#### `parse(input_path, **kwargs)`

Parse JSON file.

**Parameters**:
- `input_path` (str): JSON file path
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: MindMap object representing the parsed content

**Exceptions**:
- `ParserError`: Raised when parsing fails
- `FileNotFoundError`: Raised when file is not found

## Exception Classes

### XMindConverterError

**Description**: Base exception for XMind converter errors.

**Type**: `Exception`

### ParserError

**Description**: Exception raised when parsing fails.

**Type**: `XMindConverterError`

### ConverterError

**Description**: Exception raised when conversion fails.

**Type**: `XMindConverterError`

### FileFormatError

**Description**: Exception raised when file format is not supported.

**Type**: `XMindConverterError`

### FileNotFound

**Description**: Exception raised when file is not found.

**Type**: `XMindConverterError`

## Command Line Interface

### cli

**Description**: Command line tool main entry.

### convert

**Description**: Convert between different formats.

**Parameters**:
- `input_file`: Input file path
- `output_file`: Output file path
- `--input-format`, `-i`: Input format, supported: xmind, csv, md, html, json (optional, auto-detected from file extension)
- `--output-format`, `-o`: Output format, supported: xmind, csv, md, html, json (optional, auto-detected from file extension)

**Example**:
```bash
xmind-converter convert input.xmind output.csv
xmind-converter convert input.csv output.xmind
xmind-converter convert input.md output.html
```

### info

**Description**: Show version information.

**Parameters**: None

**Example**:
```bash
xmind-converter info
```

## Type Hints

The library includes comprehensive type hints throughout the codebase, providing:

- **Better IDE Support**: Most modern IDEs (VS Code, PyCharm, etc.) will provide intelligent autocomplete and type checking
- **Type Safety**: Use `mypy` to catch type errors before runtime
- **Documentation**: Type hints serve as inline documentation for function signatures
- **Refactoring Confidence**: Type hints make code refactoring safer and easier

### Type Checking

```bash
# Install development dependencies
uv add --dev .

# Run type checking
uv run mypy xmind_converter/
```

### Example Type-Aware Code

```python
from xmind_converter import CoreConverter, MindMap, TopicNode

# IDE will provide type hints and autocomplete
converter: CoreConverter = CoreConverter()
mindmap: MindMap = converter.load_from('example.xmind')

# Type hints help catch errors early
root: TopicNode = mindmap.topic_node
children: list[TopicNode] = root.children
```

## Security Features

### XML Security

The library uses `defusedxml` for secure XML parsing when processing XMind files (especially older XML-based formats). This provides protection against:

- **XXE Attacks**: XML External Entity attacks that can lead to information disclosure
- **Parameter Entity Attacks**: Attacks that exploit XML parameter entities
- **External DTD Retrieval**: Prevents retrieval of external DTD files

The library automatically uses `defusedxml` when available. If not installed, it falls back to the standard library with a security warning.

**Installation**: `defusedxml >= 0.7.1` is included as a core dependency and will be installed automatically with the package.
