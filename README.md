# packer

Merges codebase files into a single labeled text file. Useful for preparing project source code as context for LLMs.

## Output format

```
--- START FILE: src/packer/cli.py ---
...file contents...
--- END FILE: src/packer/cli.py ---

--- START FILE: src/packer/crawler.py ---
...
```

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Interactive mode — prompts for a path prefix filter, then extension selection
packer

# Specify root directory and output file
packer --root /path/to/project --output context.txt

# Skip prompts, include all non-binary files
packer --no-interactive

# Skip prompts, include only Python and Markdown files
packer --no-interactive -ext py -ext md
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-o`, `--output` | `codebase_context.txt` | Output file path |
| `-r`, `--root` | `.` | Root directory to crawl |
| `--no-interactive` | false | Skip prompts, process all files |
| `-ext`, `--extension` | — | Extension to include (repeatable). Only applies with `--no-interactive`. |

## Interactive flow

1. **Prefix filter** — optionally narrow files to a path prefix (e.g. `src/packer`)
2. **Extension selection** — multi-select from discovered extensions with file counts
3. **Confirmation** — shows how many files will be merged before writing

Binary files are detected heuristically (null bytes + UTF-8 decode) and skipped with a warning.

## Requirements

Python 3.8+
