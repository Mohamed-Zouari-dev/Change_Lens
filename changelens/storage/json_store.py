import json
from pathlib import Path
from typing import Dict

def save_snapshot(snapshot_data: Dict, output_path: str) -> None:
    """
    Serializes the snapshot data model and writes it to disk as a JSON file.
    """
    path = Path(output_path)
    
    # Ensure parent directories exist before saving
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        # Using indent=4 makes the JSON human-readable for debugging
        json.dump(snapshot_data, f, indent=4)

def load_snapshot(file_path: str) -> Dict:
    """
    Loads a JSON snapshot from disk back into a Python dictionary.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Snapshot file not found: '{file_path}'")
        
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)