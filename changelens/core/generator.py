from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from changelens.core.hasher import generate_file_states
from changelens.core.filters import is_excluded, load_ignore_file_patterns

def create_snapshot_model(target_dir: str, exclude_patterns: List[str] = None) -> Dict[str, Any]:
    """
    Discovers files, auto-loads local .changelensignore rules, blends them 
    with CLI exclusions, and locks them into the snapshot metadata.
    """
    if exclude_patterns is None:
        exclude_patterns = []

    target = Path(target_dir)
    
    # 1. Discover file-based patterns and merge them safely
    file_patterns = load_ignore_file_patterns(target)
    combined_patterns = list(set(exclude_patterns + file_patterns))

    discovered_files = []
    
    # 2. Discover and Filter Files
    for file in target.rglob("*"):
        if file.is_file() and not is_excluded(file, target, combined_patterns):
            discovered_files.append(file)
            
    # 3. Compute Cryptographic Hashes
    file_states = generate_file_states(str(target), discovered_files)
    
    # 4. Build and return the snapshot model
    return {
        "metadata": {
            "root_directory": str(target.resolve()),
            "timestamp": datetime.now().isoformat(),
            "total_files": len(file_states),
            "exclusions": combined_patterns  # Locked contract
        },
        "files": file_states
    }