from pathlib import Path

def get_files_in_directory(directory: str) -> list:
    """Returns a list of Path objects for all files in the directory."""
    target = Path(directory)

    if not target.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")
    if not target.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a directory.")

    # Simply collect and return the file paths
    return [file for file in target.rglob("*") if file.is_file()]