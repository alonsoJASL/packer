"""Main CLI entry point for packer."""

import sys
from pathlib import Path
from typing import List, Set

import click
import questionary

from packer.crawler import (
    crawl_directory,
    extract_extensions,
    filter_by_prefix,
    filter_by_extensions,
)
from packer.merger import merge_files


@click.command()
@click.option(
    "--output",
    "-o",
    default="codebase_context.txt",
    type=click.Path(),
    help="Output file path (default: codebase_context.txt)",
)
@click.option(
    "--root",
    "-r",
    default=".",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Root directory to crawl (default: current directory)",
)
@click.option(
    "--no-interactive",
    is_flag=True,
    help="Skip interactive prompts, process all files",
)
def main(output: str, root: str, no_interactive: bool) -> None:
    """
    Crawl directory, filter files interactively, and merge into a single labeled text file.
    
    Examples:
        packer
        packer --output context.txt --root /path/to/project
        packer --no-interactive
    """
    root_path = Path(root).resolve()
    output_path = Path(output)
    
    click.echo(f"Searching Crawling {root_path}...")
    
    # Discover all files
    all_files = list(crawl_directory(root_path))
    
    if not all_files:
        click.echo("No files found.", err=True)
        sys.exit(1)
    
    click.echo(f"Found {len(all_files)} files")
    
    # Interactive filtering
    if no_interactive:
        selected_files = all_files
    else:
        selected_files = _interactive_filter(all_files)
    
    if not selected_files:
        click.echo("No files selected after filtering.", err=True)
        sys.exit(1)
    
    # Confirmation
    if not no_interactive:
        confirmed = questionary.confirm(
            f"Merge {len(selected_files)} files into {output_path}?",
            default=True
        ).ask()
        
        if not confirmed:
            click.echo("Operation cancelled.")
            sys.exit(0)
    
    # Merge files
    merge_files(selected_files, output_path, root=root_path)


def _interactive_filter(files: List[Path]) -> List[Path]:
    """
    Run interactive filtering flow.
    
    Args:
        files: List of discovered files
        
    Returns:
        Filtered list of files based on user selections
    """
    # Step 1: Prefix filter
    prefix = questionary.text(
        "Enter a folder/file prefix to filter by (leave blank for all):",
        default=""
    ).ask()
    
    if prefix:
        files = filter_by_prefix(files, prefix)
        click.echo(f"Found {len(files)} files match prefix '{prefix}'")
    
    if not files:
        return []
    
    # Step 2: Extension selection
    extensions_dict = extract_extensions(files)
    
    # Create choices with counts
    choices = [
        questionary.Choice(
            title=f"{ext} ({count} files)",
            value=ext
        )
        for ext, count in sorted(extensions_dict.items())
    ]
    
    selected_extensions = questionary.checkbox(
        "Select file extensions to include:",
        choices=choices
    ).ask()
    
    if not selected_extensions:
        return []
    
    # Filter by selected extensions
    files = filter_by_extensions(files, set(selected_extensions))
    
    return files


if __name__ == "__main__":
    main()