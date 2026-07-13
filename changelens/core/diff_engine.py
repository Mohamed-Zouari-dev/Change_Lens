from typing import Dict, Any
from models import (
    IntegrityReport, AuditMetadata, AuditSummary, ChangeCategories,
    ModifiedFile, AddedFile, DeletedFile
)

def calculate_snapshot_diff(base_snapshot: Dict[str, Any], current_snapshot: Dict[str, Any]) -> IntegrityReport:
    """
    Compares two snapshot data models and returns a strictly typed IntegrityReport.
    """
    base_files = base_snapshot.get("files", {})
    current_files = current_snapshot.get("files", {})

    # Extract context from snapshots
    base_time = base_snapshot.get("metadata", {}).get("timestamp", "UNKNOWN")
    current_time = current_snapshot.get("metadata", {}).get("timestamp", "UNKNOWN")
    target_dir = current_snapshot.get("metadata", {}).get("root_directory", "UNKNOWN")

    changes = ChangeCategories()
    summary = AuditSummary(files_scanned=len(current_files))

    # 1. Analyze Current Files (Detect Added and Modified)
    for path, current_meta in current_files.items():
        if path not in base_files:
            changes.added.append(AddedFile(path=path, current_hash=current_meta["hash"]))
            summary.files_added += 1
        elif current_meta["hash"] != base_files[path]["hash"]:
            changes.modified.append(ModifiedFile(
                path=path,
                old_hash=base_files[path]["hash"],
                new_hash=current_meta["hash"]
            ))
            summary.files_modified += 1
        else:
            summary.files_matched += 1

    # 2. Analyze Base Files (Detect Deleted)
    for path, base_meta in base_files.items():
        if path not in current_files:
            changes.deleted.append(DeletedFile(
                path=path,
                last_known_hash=base_meta["hash"]
            ))
            summary.files_deleted += 1

    # 3. Finalize Status Metadata
    has_changes = (summary.files_added > 0 or 
                   summary.files_modified > 0 or 
                   summary.files_deleted > 0)
    
    summary.is_clean = not has_changes
    status_string = "CLEAN" if summary.is_clean else "VIOLATION_DETECTED"

    metadata = AuditMetadata(
        target_directory=target_dir,
        base_snapshot_time=base_time,
        verification_time=current_time,
        status=status_string
    )

    return IntegrityReport(
        audit_metadata=metadata,
        summary=summary,
        changes=changes
    )