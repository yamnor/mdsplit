# mdsplit: Markdown Splitter for mdBook

## Overview
`mdsplit` is a preprocessor script for mdBook, designed to parse a single long Markdown file and split it into parts, sections, and subsections. It recognizes and organizes content based on header levels: `#` for parts, `##` for sections, `###` for subsections, and retains the original levels for headers level 4 and beyond.

- The first output page is named `index.html`.
- Subsequent pages are named according to their order (e.g., `2.html`, `3.html`, etc.).
- Sections (originally level 2 headers) become level 1 headers, and subsections (originally level 3 headers) become level 2 headers in the new structure.
- Headers of level 4 and above retain their original levels after splitting.
- When a section contains subsections, the section's page includes a list of these subsections.
- If a header contains a `|`, the text string on the right side of `|` is used as the path for that page.

## Usage

To use `mdsplit` as a preprocessor in mdBook:

1. Add the following lines to your `book.toml` file:

   ```toml
   [preprocessor.mdsplit]
   command = "python mdsplit.py"
   ```

2. Ensure `mdsplit.py` is in the same directory as your `book.toml`, or adjust the command to point to its location.

## Requirements
- Python 3.x
- mdBook environment

## License
`mdsplit` is released under the ***Mozilla Public License v2.0***, for more information take a look at the [LICENSE](LICENSE) file.
