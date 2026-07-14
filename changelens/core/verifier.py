from typing import Dict, Any
from changelens.core.generator import create_snapshot_model
from changelens.core.diff_engine import calculate_snapshot_diff
from models import IntegrityReport

def verify_live_directory(stored_snapshot: Dict[str, Any], target_directory: str) -> IntegrityReport:
    """
    Generates a live snapshot using the EXACT SAME exclusions defined in the 
    historical baseline, then computes the difference.
    """
    # Extract historical rules (defaults to empty list if not found)
    historical_exclusions = stored_snapshot.get("metadata", {}).get("exclusions", [])
    
    # Generate the live representation, forcing it to use the baseline's rules
    live_snapshot = create_snapshot_model(target_directory, exclude_patterns=historical_exclusions)
    
    # Compute the diff
    return calculate_snapshot_diff(stored_snapshot, live_snapshot)