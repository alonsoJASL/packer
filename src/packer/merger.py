"""File merging and output generation logic."""

from pathlib import Path
from typing import List, TextIO


def is_likely_binary(file_path: Path, sample_size: int = 8192) -> bool:
    """
    Heuristic check if file is binary by reading first chunk.
    
    Args:
        file_path: Path to file
        sample_size: Bytes to read for check
        
    Returns:
        True if file appears binary, False otherwise
    """
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(sample_size)
            # Check for null bytes (common in binary files)
            if b"\x00" in chunk:
                return True
            # Try to decode as UTF-8
            chunk.decode("utf-8")
            return False
    except (UnicodeDecodeError, PermissionError):
        return True


def merge_files(
    files: List[Path],
    output_path: Path = Path("codebase_context.txt"),
    root: Path = Path("."),
    skip_binary: bool = True
) -> None:
    """
    Merge multiple files into single output with delimiters.
    
    Args:
        files: List of Path objects to merge
        output_path: Destination file
        root: Root directory for relative path calculation
        skip_binary: If True, skip binary files with warning
    """
    skipped_count = 0
    
    with open(output_path, "w", encoding="utf-8") as outfile:
        for file_path in files:
            if skip_binary and is_likely_binary(file_path):
                print(f"WARNING Skipping binary file: {file_path.relative_to(root)}")
                skipped_count += 1
                continue
            
            try:
                _write_file_section(outfile, file_path, root)
            except Exception as e:
                print(f"Error reading {file_path.relative_to(root)}: {e}")
                skipped_count += 1
    
    print(f"\nMerged {len(files) - skipped_count} files into {output_path}")
    if skipped_count > 0:
        print(f"WARNING Skipped {skipped_count} files (binary or unreadable)")

def _write_file_section(outfile: TextIO, file_path: Path, root: Path) -> None:
    """
    Write a single file's content with delimiters.
    
    Args:
        outfile: Open file handle for output
        file_path: Path to source file
        root: Root directory to compute relative path from
    """
    relative_path = file_path.relative_to(root)
    outfile.write(f"--- START FILE: {relative_path} ---\n")
    
    with open(file_path, "r", encoding="utf-8", errors="replace") as infile:
        outfile.write(infile.read())
    
    outfile.write("\n")
    outfile.write(f"--- END FILE: {relative_path} ---\n\n")