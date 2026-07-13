from typing import Dict, Any
from core.generator import create_snapshot_model
from core.diff_engine import calculate_snapshot_diff

def verify_live_directory(stored_snapshot: Dict[str, Any], target_directory: str) -> Dict[str, Any]:
    """
    Generates a live snapshot of a directory and computes its differences 
    against a historically stored snapshot structure.
    """
    # Generate the live representation of the filesystem
    live_snapshot = create_snapshot_model(target_directory)
    
    # Compute the diff using the pure engine
    return calculate_snapshot_diff(stored_snapshot, live_snapshot)