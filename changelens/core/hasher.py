import hashlib
from pathlib import Path
from typing import Dict, Union, List

def hash_file(file_path: Union[str, Path]) -> str:
    """Hashes a single file efficiently in chunks to prevent memory bloat."""
    hash_func = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

def generate_file_states(target_dir: str, files: List[Path]) -> Dict[str, dict]:
    target = Path(target_dir)
    file_states = {}
    
    for file in files:
        try:
            rel_path = str(file.relative_to(target))
            
            file_states[rel_path] = {
                "hash": hash_file(file)
            }
            
        except PermissionError:
            print(f"Warning: Permission denied for '{file}'. Skipping.")
        except Exception as e:
            print(f"Warning: Could not process '{file}': {e}")
            
    return file_states