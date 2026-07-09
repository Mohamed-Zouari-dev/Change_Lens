import hashlib
from pathlib import Path

def hash_file(file_path: str | Path) -> str:
    """Hashes a single file efficiently in chunks."""
    hash_func = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

def generate_snapshot_dict(target_dir: str, files: list) -> dict:
    """Iterates through a list of files and returns a {relative_path: hash} dictionary."""
    target = Path(target_dir)
    snapshot = {}
    
    for file in files:
        try:
            # 1. Calculate the hash using your existing function
            file_hash = hash_file(file)
            
            # 2. Determine the relative path string
            rel_path = str(file.relative_to(target))
            
            # 3. Add to dictionary
            snapshot[rel_path] = file_hash
            
        except PermissionError:
            print(f"Warning: Permission denied for {file}. Skipping.")
        except Exception as e:
            print(f"Warning: Could not process {file}: {e}")
            
    return snapshot