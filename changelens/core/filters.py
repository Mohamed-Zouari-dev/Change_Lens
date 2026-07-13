import fnmatch
from pathlib import Path
from typing import List

def is_excluded(file_path: Path, base_dir: Path, exclude_patterns: List[str]) -> bool:
    """
    Checks if a file matches any of the provided exclusion glob patterns.
    Matches against both the exact filename and the relative path.
    """
    if not exclude_patterns:
        return False
        
    rel_path = file_path.relative_to(base_dir).as_posix()
    
    for pattern in exclude_patterns:
        # Check against filename (e.g., "*.log") or relative path (e.g., "node_modules/*")
        if fnmatch.fnmatch(file_path.name, pattern) or fnmatch.fnmatch(rel_path, pattern):
            return True
            
    return False