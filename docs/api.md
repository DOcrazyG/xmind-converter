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

#### `load_from(input_path, format_type=None, **kwargs)`

Load from specified format and convert to MindMap.

**Parameters**:
- `input_path` (str): Path to the input file
- `format_type` (str, optional): Format type (auto-detected from file extension if not provided). Supported: 'xmind', 'csv', 'md', 'html', 'json'
- `**kwargs`: Additional format-specific parameters

**Return Value**: `MindMap` object representing the parsed content

**Exceptions**:
- `XMindConverterError`: Raised when loading fails or format is unsupported

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

**Exceptions**:
- `XMindConverterError`: Raised when conversion fails or format is unsupported

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

**Exceptions**:
- `XMindConverterError`: Raised when conversion fails or format is unsupported

**Example**:
```python
converter = CoreConverter()
result = converter.convert('input.xmind', 'output.csv')
result = converter.convert('input.csv', 'output.xmind')
result = converter.convert('input.md', 'output.html')
```

## Data Models

### MindMap

**Description**: Mind map class representing the entire mind map structure.

**Methods**:

#### `__init__(name, root_node=None)`

Initialize MindMap instance.

**Parameters**:
- `name` (str): Mind map name
- `root_node` (MindNode, optional): Root node of the mind map

**Return Value**: MindMap instance

#### `__str__()`

Get string representation of the mind map.

**Parameters**: None

**Return Value**: str - String representation

#### `__repr__()`

Get detailed string representation of the mind map.

**Parameters**: None

**Return Value**: str - Detailed string representation

#### `print_tree()`

Print the mind map tree structure.

**Parameters**: None

**Return Value**: None

### MindNode

**Description**: Mind map node class, used to represent nodes in mind maps.

**Methods**:

#### `__init__(title, node_id=None, children=None, parent=None)`

Initialize node instance.

**Parameters**:
- `title` (str): Node title
- `node_id` (str, optional): Node ID
- `children` (list, optional): Child node list
- `parent` (MindNode, optional): Parent node

**Return Value**: MindNode instance

#### `add_child(child)`

Add child node.

**Parameters**:
- `child` (MindNode): Child node object

**Return Value**: None

#### `get_depth()`

Get node depth.

**Parameters**: None

**Return Value**: int - Node depth

#### `__str__()`

Get string representation of the node.

**Parameters**: None

**Return Value**: str - String representation

#### `__repr__()`

Get detailed string representation of the node.

**Parameters**: None

**Return Value**: str - Detailed string representation

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

Convert MindMap to Markdown format and save to file.

**Parameters**:
- `mindmap` (MindMap): MindMap object to convert
- `output_path` (str): Path to save the Markdown file
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: None

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

Convert MindMap to JSON format and save to file.

**Parameters**:
- `mindmap` (MindMap): MindMap object to convert
- `output_path` (str): Path to save the JSON file
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: None

### XMindFileConverter

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

**Methods**:

#### `parse(input_path, **kwargs)`

Parse XMind file.

**Parameters**:
- `input_path` (str): XMind file path
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: MindMap object representing the parsed content

**Exceptions**:
- `XMindConverterError`: Raised when parsing fails

### CSVParser

**Description**: CSV file parser.

**Methods**:

#### `parse(input_path, **kwargs)`

Parse CSV file.

**Parameters**:
- `input_path` (str): CSV file path
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: MindMap object representing the parsed content

**Exceptions**:
- `XMindConverterError`: Raised when parsing fails

### MarkdownParser

**Description**: Markdown file parser.

**Methods**:

#### `parse(input_path, **kwargs)`

Parse Markdown file.

**Parameters**:
- `input_path` (str): Markdown file path
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: MindMap object representing the parsed content

**Exceptions**:
- `XMindConverterError`: Raised when parsing fails

### HTMLParser

**Description**: HTML file parser.

**Methods**:

#### `parse(input_path, **kwargs)`

Parse HTML file.

**Parameters**:
- `input_path` (str): HTML file path
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: MindMap object representing the parsed content

**Exceptions**:
- `XMindConverterError`: Raised when parsing fails

### JSONParser

**Description**: JSON file parser.

**Methods**:

#### `parse(input_path, **kwargs)`

Parse JSON file.

**Parameters**:
- `input_path` (str): JSON file path
- `**kwargs`: Additional parameters (not currently used)

**Return Value**: MindMap object representing the parsed content

**Exceptions**:
- `XMindConverterError`: Raised when parsing fails

## Exception Classes

### XMindConverterError

**Description**: Base exception for XMind converter errors.

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
