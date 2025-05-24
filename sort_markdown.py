#!/usr/bin/env python3
"""
Markdown Section Sorter

This script reads a Markdown file and recursively sorts all sections alphabetically.
First-level sections are sorted, then within each section, sub-sections are sorted recursively.
"""

import re
import sys
from typing import List, Tuple, Optional


class MarkdownSection:
    """Represents a section in a Markdown document."""
    
    def __init__(self, title: str, level: int, content: List[str]):
        self.title = title
        self.level = level
        self.content = content
        self.subsections: List['MarkdownSection'] = []
    
    def add_content_line(self, line: str):
        """Add a line of content to this section."""
        self.content.append(line)
    
    def add_subsection(self, subsection: 'MarkdownSection'):
        """Add a subsection to this section."""
        self.subsections.append(subsection)
    
    def sort_subsections(self):
        """Recursively sort all subsections alphabetically by title."""
        self.subsections.sort(key=lambda s: s.title.lower())
        for subsection in self.subsections:
            subsection.sort_subsections()
    
    def to_markdown(self) -> str:
        """Convert this section back to Markdown format."""
        result = []
        
        # Add the section header
        result.append('#' * self.level + ' ' + self.title)
        
        # Add the content
        result.extend(self.content)
        
        # Add subsections
        for subsection in self.subsections:
            result.append(subsection.to_markdown())
        
        return '\n'.join(result)


class MarkdownSorter:
    """Sorts Markdown sections recursively."""
    
    def __init__(self):
        self.header_pattern = re.compile(r'^(#+)\s+(.+)$')
    
    def parse_markdown(self, lines: List[str]) -> Tuple[List[str], List[MarkdownSection]]:
        """Parse Markdown lines into a preamble and sections."""
        preamble = []
        sections = []
        current_section = None
        section_stack = []
        
        for line in lines:
            match = self.header_pattern.match(line)
            
            if match:
                # Found a header
                level = len(match.group(1))
                title = match.group(2).strip()
                
                new_section = MarkdownSection(title, level, [])
                
                # Find the appropriate parent section
                while section_stack and section_stack[-1].level >= level:
                    section_stack.pop()
                
                if section_stack:
                    # This is a subsection
                    section_stack[-1].add_subsection(new_section)
                else:
                    # This is a top-level section
                    sections.append(new_section)
                
                section_stack.append(new_section)
                current_section = new_section
            else:
                # Regular content line
                if current_section is None:
                    # Before any section - this is preamble
                    preamble.append(line)
                else:
                    # Add to current section
                    current_section.add_content_line(line)
        
        return preamble, sections
    
    def sort_markdown(self, content: str) -> str:
        """Sort all sections in the Markdown content recursively."""
        lines = content.split('\n')
        
        # Parse the markdown
        preamble, sections = self.parse_markdown(lines)
        
        # Sort top-level sections
        sections.sort(key=lambda s: s.title.lower())
        
        # Recursively sort subsections
        for section in sections:
            section.sort_subsections()
        
        # Reconstruct the document
        result = []
        
        # Add preamble
        if preamble:
            result.extend(preamble)
            # Add a newline after preamble if there are sections
            if sections and preamble[-1].strip():
                result.append('')
        
        # Add sorted sections
        for i, section in enumerate(sections):
            if i > 0:
                # Add blank line between top-level sections
                result.append('')
            result.append(section.to_markdown())
        
        return '\n'.join(result)
    
    def sort_file(self, input_path: str, output_path: Optional[str] = None):
        """Sort a Markdown file."""
        # Read the input file
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File '{input_path}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
        
        # Sort the content
        sorted_content = self.sort_markdown(content)
        
        # Determine output path
        if output_path is None:
            output_path = input_path
        
        # Write the output
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(sorted_content)
            print(f"Successfully sorted Markdown sections in '{output_path}'")
        except Exception as e:
            print(f"Error writing file: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python sort_markdown.py <input_file> [output_file]")
        print("If output_file is not specified, the input file will be overwritten.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    sorter = MarkdownSorter()
    sorter.sort_file(input_file, output_file)


if __name__ == "__main__":
    main()