from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from core.hasher import generate_file_states
from core.filters import is_excluded

def create_snapshot_model(target_dir: str, exclude_patterns: List[str] = None) -> Dict[str, Any]:
    """
    Discovers files, applies exclusion filters, and builds the snapshot dictionary.
    """
    if exclude_patterns is None:
        exclude_patterns = []

    target = Path(target_dir)
    discovered_files = []
    
    # 1. Discover and Filter Files
    for file in target.rglob("*"):
        if file.is_file() and not is_excluded(file, target, exclude_patterns):
            discovered_files.append(file)
            
    # 2. Compute Cryptographic Hashes
    file_states = generate_file_states(str(target), discovered_files)
    
    # 3. Build and return the snapshot model
    return {
        "metadata": {
            "root_directory": str(target.resolve()),
            "timestamp": datetime.now().isoformat(),
            "total_files": len(file_states),
            "exclusions": exclude_patterns  # <-- Saved to the baseline!
        },
        "files": file_states
    }