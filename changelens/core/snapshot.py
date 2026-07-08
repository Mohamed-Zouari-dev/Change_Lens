from pathlib import Path

def scan_directory(directory: str) -> list:
    target = Path(directory)

    if not target.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    if not target.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a directory.")

    files = [
        file.resolve()
        for file in target.rglob("*")
        if file.is_file()
    ]

    return sorted(files)