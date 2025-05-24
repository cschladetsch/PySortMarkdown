#!/usr/bin/env python3
"""
Test runner for PySortMarkdown
"""

import os
import sys
import shutil
import difflib
from pathlib import Path
from sort_markdown import MarkdownSorter


class TestRunner:
    def __init__(self):
        self.sorter = MarkdownSorter()
        self.test_dir = Path("test_output")
        self.passed = 0
        self.failed = 0
    
    def setup(self):
        """Create test output directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
    
    def run_test(self, test_name: str, input_file: str, expected_output: str = None):
        """Run a single test."""
        print(f"\nRunning test: {test_name}")
        print("-" * 50)
        
        try:
            # Read input
            with open(input_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Sort content
            sorted_content = self.sorter.sort_markdown(original_content)
            
            # Save output
            output_file = self.test_dir / f"{Path(input_file).stem}_sorted.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(sorted_content)
            
            # If expected output provided, compare
            if expected_output and os.path.exists(expected_output):
                with open(expected_output, 'r', encoding='utf-8') as f:
                    expected = f.read()
                
                if sorted_content == expected:
                    print(f"✓ Test passed: Output matches expected")
                    self.passed += 1
                else:
                    print(f"✗ Test failed: Output differs from expected")
                    self.failed += 1
                    # Show diff
                    diff = difflib.unified_diff(
                        expected.splitlines(keepends=True),
                        sorted_content.splitlines(keepends=True),
                        fromfile='expected',
                        tofile='actual'
                    )
                    print(''.join(diff))
            else:
                # Just verify it runs without error
                print(f"✓ Test passed: Sorted successfully")
                print(f"  Output saved to: {output_file}")
                self.passed += 1
                
                # Show first few lines of output
                lines = sorted_content.split('\n')
                preview_lines = min(10, len(lines))
                print(f"\n  Preview (first {preview_lines} lines):")
                for i, line in enumerate(lines[:preview_lines]):
                    print(f"    {i+1:3d}: {line}")
                if len(lines) > preview_lines:
                    print(f"    ... ({len(lines) - preview_lines} more lines)")
        
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            self.failed += 1
    
    def verify_sorting_properties(self, content: str):
        """Verify that sections are properly sorted."""
        lines = content.split('\n')
        headers = []
        
        for line in lines:
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                headers.append((level, title))
        
        # Check if top-level headers are sorted
        top_level = [(level, title) for level, title in headers if level == 1]
        sorted_top = sorted(top_level, key=lambda x: x[1].lower())
        
        return top_level == sorted_top
    
    def run_all_tests(self):
        """Run all tests."""
        print("PySortMarkdown Test Suite")
        print("=" * 50)
        
        self.setup()
        
        # Test files
        test_files = [
            ("Basic Sorting", "test/test_basic.md"),
            ("Nested Sections", "test/test_nested.md"),
            ("Mixed Content", "test/test_mixed.md"),
            ("Unicode Support", "test/test_unicode.md"),
            ("Edge Cases", "test/test_edge_cases.md"),
            ("Original Test", "test/test_input.md"),
        ]
        
        for test_name, test_file in test_files:
            if os.path.exists(test_file):
                self.run_test(test_name, test_file)
            else:
                print(f"\n✗ Test file not found: {test_file}")
                self.failed += 1
        
        # Summary
        print("\n" + "=" * 50)
        print(f"Test Summary: {self.passed} passed, {self.failed} failed")
        print(f"Total tests: {self.passed + self.failed}")
        
        return self.failed == 0


def main():
    """Main entry point."""
    runner = TestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()