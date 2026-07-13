from pathlib import Path
from typing import List

def get_files_in_directory(directory: str) -> List[Path]:
    target = Path(directory)

    if not target.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")
    if not target.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a directory.")

    return [file for file in target.rglob("*") if file.is_file()]