# PySortMarkdown

A Python tool that recursively sorts Markdown sections alphabetically while preserving document structure and content.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Examples](#examples)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Edge Cases](#edge-cases)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Recursive Sorting**: Sorts sections at all levels of hierarchy
- **Structure Preservation**: Maintains the hierarchical structure of your document
- **Content Preservation**: All content within sections remains unchanged
- **Preamble Support**: Content before the first section is preserved
- **Unicode Support**: Handles international characters correctly
- **Flexible Output**: Can overwrite the original file or create a new sorted file
- **Clean Output**: Maintains proper spacing between sections

## Installation

1. Ensure you have Python 3.6 or higher installed:
```bash
python3 --version
```

2. Clone or download the repository:
```bash
git clone https://github.com/yourusername/PySortMarkdown.git
cd PySortMarkdown
```

3. No additional dependencies required! The tool uses only Python standard library.

## Usage

### Basic Usage

Sort a Markdown file in-place:
```bash
python3 sort_markdown.py document.md
```

Sort a Markdown file to a new file:
```bash
python3 sort_markdown.py input.md output.md
```

### Command Line Interface

```
Usage: python3 sort_markdown.py <input_file> [output_file]

Arguments:
  input_file   - Path to the Markdown file to sort
  output_file  - (Optional) Path for the sorted output
                 If not specified, the input file will be overwritten
```

## How It Works

### Sorting Algorithm

1. **Parsing Phase**:
   - Identifies headers using regex pattern `^(#+)\s+(.+)$`
   - Builds a hierarchical tree structure of sections
   - Preserves content before the first header as "preamble"

2. **Sorting Phase**:
   - Sorts top-level sections alphabetically (case-insensitive)
   - Recursively sorts subsections within each section
   - Maintains parent-child relationships

3. **Reconstruction Phase**:
   - Rebuilds the document with sorted sections
   - Preserves original formatting and content
   - Adds appropriate spacing between sections

### Section Detection

The tool recognizes standard Markdown headers:
- `# Level 1 Header`
- `## Level 2 Header`
- `### Level 3 Header`
- And so on...

## Examples

### Example 1: Basic Sorting

**Input** (`unsorted.md`):
```markdown
# Introduction

Some introductory text.

# Zebra

Information about zebras.

## Diet
What zebras eat.

## Habitat
Where zebras live.

# Apple

Information about apples.

## Varieties
Different types of apples.

## Nutrition
Nutritional value of apples.
```

**Output** (`sorted.md`):
```markdown
# Apple

Information about apples.

## Nutrition
Nutritional value of apples.

## Varieties
Different types of apples.

# Introduction

Some introductory text.

# Zebra

Information about zebras.

## Diet
What zebras eat.

## Habitat
Where zebras live.
```

### Example 2: Nested Sections

**Input**:
```markdown
# Chapter 3

## Section 3.2

### Subsection 3.2.3
Content

### Subsection 3.2.1
Content

## Section 3.1

# Chapter 1

## Section 1.2

## Section 1.1
```

**Output**:
```markdown
# Chapter 1

## Section 1.1

## Section 1.2

# Chapter 3

## Section 3.1

## Section 3.2

### Subsection 3.2.1
Content

### Subsection 3.2.3
Content
```

### Example 3: Document with Preamble

**Input**:
```markdown
---
title: My Document
author: John Doe
---

This document contains various sections that need sorting.

# Conclusion

Final thoughts.

# Abstract

Summary of the document.

# Introduction

Opening remarks.
```

**Output**:
```markdown
---
title: My Document
author: John Doe
---

This document contains various sections that need sorting.

# Abstract

Summary of the document.

# Conclusion

Final thoughts.

# Introduction

Opening remarks.
```

## API Documentation

### Classes

#### `MarkdownSection`

Represents a section in a Markdown document.

**Attributes**:
- `title` (str): The section title (without the # symbols)
- `level` (int): The heading level (1 for #, 2 for ##, etc.)
- `content` (List[str]): Lines of content within this section
- `subsections` (List[MarkdownSection]): Child sections

**Methods**:
- `add_content_line(line: str)`: Add a line of content to this section
- `add_subsection(subsection: MarkdownSection)`: Add a subsection
- `sort_subsections()`: Recursively sort all subsections alphabetically
- `to_markdown() -> str`: Convert section back to Markdown format

#### `MarkdownSorter`

Main class for sorting Markdown documents.

**Methods**:
- `parse_markdown(lines: List[str]) -> Tuple[List[str], List[MarkdownSection]]`: Parse Markdown lines into preamble and sections
- `sort_markdown(content: str) -> str`: Sort all sections in the Markdown content
- `sort_file(input_path: str, output_path: Optional[str] = None)`: Sort a Markdown file

### Usage in Python Code

```python
from sort_markdown import MarkdownSorter

# Create a sorter instance
sorter = MarkdownSorter()

# Sort a string containing Markdown
markdown_content = """
# Zebra
Content

# Apple
Content
"""
sorted_content = sorter.sort_markdown(markdown_content)

# Sort a file
sorter.sort_file('input.md', 'output.md')
```

## Testing

### Running Tests

Create test files and run the sorting tool:

```bash
# Test basic sorting
python3 sort_markdown.py test_input.md test_output.md

# Test in-place sorting (make a backup first!)
cp important.md important.backup.md
python3 sort_markdown.py important.md
```

### Test Cases

We provide several test files to validate different scenarios:

1. **test_basic.md** - Basic section sorting
2. **test_nested.md** - Deeply nested sections
3. **test_mixed.md** - Mixed content types
4. **test_unicode.md** - International characters
5. **test_edge_cases.md** - Various edge cases

### Creating Test Files

The repository includes the following test files:

1. **test_basic.md** - Tests basic alphabetical sorting of sections
2. **test_nested.md** - Tests deeply nested section hierarchies
3. **test_mixed.md** - Tests sorting with various Markdown elements (code blocks, tables, lists)
4. **test_unicode.md** - Tests international character support
5. **test_edge_cases.md** - Tests various edge cases and unusual scenarios

### Running the Test Suite

Run all tests using the test runner:

```bash
python3 run_tests.py
```

This will:
- Execute all test files
- Save sorted outputs to `test_output/` directory
- Display test results and any failures
- Show preview of sorted content

### Manual Testing

Test individual files:

```bash
# Test basic sorting
python3 sort_markdown.py test_basic.md test_output/basic_sorted.md

# Test unicode handling
python3 sort_markdown.py test_unicode.md test_output/unicode_sorted.md

# Test edge cases
python3 sort_markdown.py test_edge_cases.md test_output/edges_sorted.md
```

## Edge Cases

The tool handles these edge cases gracefully:

1. **Empty Headers**: Headers with just `#` and spaces are preserved
2. **Headers with Special Characters**: Code backticks, bold, italic formatting in headers
3. **Duplicate Headers**: Multiple sections with same title are preserved (stable sort)
4. **Non-standard Headers**: Lines starting with `#` without space are not treated as headers
5. **Unicode Characters**: Full support for international characters in headers and content
6. **Mixed Case**: Case-insensitive sorting (e.g., "apple" and "Apple" sort together)
7. **Nested Structures**: Maintains proper parent-child relationships regardless of depth
8. **Preamble Content**: Everything before first header is preserved as-is
9. **Trailing Spaces**: Automatically trimmed from headers
10. **Empty Sections**: Sections with no content are preserved

## Limitations

- **Setext Headers**: Only ATX-style headers (`#`) are supported, not Setext-style (underlined)
- **Header Levels**: Standard Markdown supports levels 1-6, though the tool will handle more
- **Performance**: For extremely large files (>10MB), processing may take a few seconds
- **Memory**: Entire file is loaded into memory during processing

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite (`python3 run_tests.py`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Maintain backward compatibility
- Add tests for new features
- Follow PEP 8 style guidelines
- Update documentation as needed
- Keep dependencies minimal (preferably none)

## License

This project is released into the public domain. You are free to use, modify, and distribute it as you wish.

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release
- Recursive section sorting
- Unicode support
- Comprehensive test suite
- Full documentation

## Acknowledgments

- Inspired by the need for organized documentation
- Built with Python's excellent standard library
- Tested with various real-world Markdown documents

---

For bug reports or feature requests, please open an issue on GitHub.