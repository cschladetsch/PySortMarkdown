# Edge Case Testing

This file tests various edge cases.

#Not A Header (missing space)

This should not be treated as a header.

# 

Empty header above (just space after #).

# Header with ### symbols in title

Content here.

# Header with `code` in title

Content with inline code.

# Header with **bold** and *italic*

Content here.

# Very Long Header That Goes On And On And On And Contains Many Words To Test How The System Handles Extended Header Text

Content for long header.

###### Level 6 Header

Deepest standard header level.

####### Level 7 Header (Non-standard)

This might not be recognized by all parsers.

# Duplicate Header

First occurrence.

# Duplicate Header

Second occurrence (should sort together).

# 123 Numeric Start

Headers starting with numbers.

# _Underscore Start

Headers starting with special characters.

# [Bracket] Header

Headers with brackets.

# Header (with parentheses)

Headers with parentheses.

# Header with trailing spaces    

This header has trailing spaces (which should be trimmed).

#    Header with leading spaces

This header has spaces after the # symbol.

# Mixed-Case HEADER

Testing case-insensitive sorting.

# mixed-case header

Should sort near the above header.

# 

Another empty header.

## Subsection without parent ending

This subsection appears at the end without more content.