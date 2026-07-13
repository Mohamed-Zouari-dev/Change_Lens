from typing import Dict, Any

def calculate_snapshot_diff(base_snapshot: Dict[str, Any], current_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compares two snapshot data models (base vs current).
    
    Returns a structured dictionary containing metadata changes and 
    categorized file modifications (added, deleted, modified).
    """
    base_files = base_snapshot.get("files", {})
    current_files = current_snapshot.get("files", {})

    diff_report = {
        "summary": {
            "base_timestamp": base_snapshot.get("metadata", {}).get("timestamp"),
            "current_timestamp": current_snapshot.get("metadata", {}).get("timestamp"),
            "added_count": 0,
            "deleted_count": 0,
            "modified_count": 0
        },
        "added": [],
        "deleted": [],
        "modified": []
    }

    # 1. Analyze Current Files (Detect Added and Modified)
    for path, current_meta in current_files.items():
        if path not in base_files:
            diff_report["added"].append({
                "path": path,
                "current_hash": current_meta["hash"]
            })
        elif current_meta["hash"] != base_files[path]["hash"]:
            diff_report["modified"].append({
                "path": path,
                "old_hash": base_files[path]["hash"],
                "new_hash": current_meta["hash"]
            })

    # 2. Analyze Base Files (Detect Deleted)
    for path, base_meta in base_files.items():
        if path not in current_files:
            diff_report["deleted"].append({
                "path": path,
                "last_known_hash": base_meta["hash"]
            })

    # 3. Populate Summary Counts
    diff_report["summary"]["added_count"] = len(diff_report["added"])
    diff_report["summary"]["deleted_count"] = len(diff_report["deleted"])
    diff_report["summary"]["modified_count"] = len(diff_report["modified"])

    return diff_report