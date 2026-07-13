from datetime import datetime
from pathlib import Path
from typing import Dict

from core.snapshot import get_files_in_directory
from core.hasher import generate_file_states

def create_snapshot_model(directory: str) -> Dict:
    """
    Orchestrates the creation of a full snapshot data model, combining 
    file discovery, state generation, and contextual metadata.
    """
    # 1. Discover all files
    files = get_files_in_directory(directory)
    
    # 2. Generate states (hashes and mtimes)
    file_states = generate_file_states(directory, files)
    
    # 3. Assemble the Data Model
    snapshot_model = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "root_directory": str(Path(directory).resolve()),
            "total_files": len(file_states)
        },
        "files": file_states
    }
    
    return snapshot_model