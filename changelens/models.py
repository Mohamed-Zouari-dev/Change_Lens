from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class ModifiedFile:
    path: str
    old_hash: str
    new_hash: str

@dataclass
class AddedFile:
    path: str
    current_hash: str

@dataclass
class DeletedFile:
    path: str
    last_known_hash: str

@dataclass
class AuditMetadata:
    target_directory: str
    base_snapshot_time: str
    verification_time: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "CLEAN"  

@dataclass
class AuditSummary:
    files_scanned: int = 0
    files_matched: int = 0
    files_modified: int = 0
    files_added: int = 0
    files_deleted: int = 0
    is_clean: bool = True

@dataclass
class ChangeCategories:
    modified: List[ModifiedFile] = field(default_factory=list)  # Restored
    added: List[AddedFile] = field(default_factory=list)
    deleted: List[DeletedFile] = field(default_factory=list)

@dataclass
class IntegrityReport:
    audit_metadata: AuditMetadata
    summary: AuditSummary
    changes: ChangeCategories