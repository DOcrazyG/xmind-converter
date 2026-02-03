# API Documentation

This document provides detailed API reference for the XMind Converter library.

## Core Classes

### XMindConverter

**Description**: Main XMind converter class, used for loading XMind files and performing format conversions.

**Methods**:

#### `__init__()`

Initialize converter instance.

**Parameters**: None

**Return Value**: Converter instance

#### `load_xmind(file_path)`

Load XMind file and parse into node tree.

**Parameters**:
- `file_path` (str): XMind file path

**Return Value**: `Node` object representing the parsed root node

**Exceptions**:
- `XMindConverterError`: Raised when loading fails

#### `convert_to(node, format_type, output_path=None, **kwargs)`

Convert node tree to specified format.

**Parameters**:
- `node` (Node): Node to convert
- `format_type` (str): Output format, supporting 'csv', 'md', 'html', 'json'
- `output_path` (str, optional): Output file path, returns converted content if None
- `**kwargs`: Additional conversion parameters

**Return Value**:
- If `output_path` is specified, returns success message string
- If `output_path` is not specified, returns converted content string

**Exceptions**:
- `XMindConverterError`: Raised when conversion fails

#### `convert_from(input_path, format_type, output_path=None, **kwargs)`

Convert from specified format to node tree.

**Parameters**:
- `input_path` (str): Input file path
- `format_type` (str): Input format, supporting 'csv', 'md', 'html', 'json'
- `output_path` (str, optional): Output XMind file path
- `**kwargs`: Additional conversion parameters

**Return Value**:
- `Node` object representing the converted root node

**Exceptions**:
- `XMindConverterError`: Raised when conversion fails

### Node

**Description**: Mind map node class, used to represent nodes in XMind files.

**Methods**:

#### `__init__(title, children=None, attributes=None)`

Initialize node instance.

**Parameters**:
- `title` (str): Node title
- `children` (list, optional): Child node list
- `attributes` (dict, optional): Node attribute dictionary

**Return Value**: Node instance

#### `add_child(child)`

Add child node.

**Parameters**:
- `child` (Node): Child node object

**Return Value**: None

#### `get_depth()`

Get node depth.

**Parameters**: None

**Return Value**: int representing node depth

#### `traverse(callback, depth=0)`

Traverse node tree.

**Parameters**:
- `callback` (function): Callback function that receives node and depth as parameters
- `depth` (int, optional): Starting depth

**Return Value**: None

## Converter Classes

### CSVConverter

**Description**: CSV format converter.

**Methods**:

#### `convert(node, delimiter=',')`

Convert node to CSV format.

**Parameters**:
- `node` (Node): Node to convert
- `delimiter` (str, optional): CSV delimiter, default is ','

**Return Value**: str representing CSV format content

#### `convert_from(input_path, delimiter=',')`

Convert from CSV format to node.

**Parameters**:
- `input_path` (str): CSV file path
- `delimiter` (str, optional): CSV delimiter, default is ','

**Return Value**: Node object representing the converted root node

### MarkdownConverter

**Description**: Markdown format converter.

**Methods**:

#### `convert(node)`

Convert node to Markdown format.

**Parameters**:
- `node` (Node): Node to convert

**Return Value**: str representing Markdown format content

#### `convert_from(input_path)`

Convert from Markdown format to node.

**Parameters**:
- `input_path` (str): Markdown file path

**Return Value**: Node object representing the converted root node

### HTMLConverter

**Description**: HTML format converter.

**Methods**:

#### `convert(node)`

Convert node to HTML format.

**Parameters**:
- `node` (Node): Node to convert

**Return Value**: str representing HTML format content

#### `convert_from(input_path)`

Convert from HTML format to node (not implemented yet).

**Parameters**:
- `input_path` (str): HTML file path

**Return Value**: None

**Exceptions**:
- `NotImplementedError`: Method not implemented

### JSONConverter

**Description**: JSON format converter.

**Methods**:

#### `convert(node)`

Convert node to JSON format.

**Parameters**:
- `node` (Node): Node to convert

**Return Value**: str representing JSON format content

#### `convert_from(input_path)`

Convert from JSON format to node.

**Parameters**:
- `input_path` (str): JSON file path

**Return Value**: Node object representing the converted root node

## Parser Classes

### XMindParser

**Description**: XMind file parser.

**Methods**:

#### `parse(file_path)`

Parse XMind file.

**Parameters**:
- `file_path` (str): XMind file path

**Return Value**: Node object representing the parsed root node

**Exceptions**:
- `XMindParserError`: Raised when parsing fails

## Exception Classes

### XMindConverterError

**Description**: XMind converter base exception.

### XMindParserError

**Description**: XMind parsing exception.

### ConverterError

**Description**: Conversion exception.

### FileFormatError

**Description**: File format exception.

### FileNotFoundError

**Description**: File not found exception.

## Command Line Interface

### cli

**Description**: Command line tool main entry.

### convert

**Description**: Convert XMind file to other formats.

**Parameters**:
- `input_file`: Input XMind file path
- `output_file`: Output file path
- `--format`, `-f`: Output format, supporting: csv, md, html, json

### reverse

**Description**: Convert from other formats to XMind file.

**Parameters**:
- `input_file`: Input file path
- `output_file`: Output XMind file path
- `--format`, `-f`: Input format, supporting: csv, md, html, json

### info

**Description**: Show version information.

**Parameters**: None