"""File discovery and filtering logic."""

from pathlib import Path
from typing import Generator, Dict, Set, List


# Directories to ignore during crawl
DEFAULT_IGNORE = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    "htmlcov",
}


def crawl_directory(
    root: Path = Path("."),
    ignore_dirs: Set[str] = DEFAULT_IGNORE
) -> Generator[Path, None, None]:
    """
    Recursively crawl directory and yield file paths.
    
    Args:
        root: Starting directory (default: current directory)
        ignore_dirs: Set of directory names to skip
        
    Yields:
        Path objects for each discovered file
    """
    for item in root.rglob("*"):
        # Skip if any parent directory is in ignore list
        if any(parent.name in ignore_dirs for parent in item.parents):
            continue
        
        if item.is_file():
            yield item


def extract_extensions(files: List[Path]) -> Dict[str, int]:
    """
    Extract unique file extensions and count occurrences.
    
    Args:
        files: List of Path objects
        
    Returns:
        Dictionary mapping extension to count, e.g. {".py": 42, "NO_EXT": 3}
    """
    ext_count: Dict[str, int] = {}
    
    for file_path in files:
        ext = file_path.suffix if file_path.suffix else "NO_EXT"
        ext_count[ext] = ext_count.get(ext, 0) + 1
    
    return ext_count


def filter_by_prefix(files: List[Path], prefix: str) -> List[Path]:
    """
    Filter files by path prefix.
    
    Args:
        files: List of Path objects
        prefix: Prefix string to match (e.g., "pycemrg")
        
    Returns:
        Filtered list of Path objects
    """
    if not prefix:
        return files
    
    return [f for f in files if str(f).startswith(prefix)]


def filter_by_extensions(files: List[Path], extensions: Set[str]) -> List[Path]:
    """
    Filter files by extension set.
    
    Args:
        files: List of Path objects
        extensions: Set of extensions to include (e.g., {".py", ".cpp"})
        
    Returns:
        Filtered list of Path objects
    """
    return [
        f for f in files
        if (f.suffix in extensions) or (f.suffix == "" and "NO_EXT" in extensions)
    ]