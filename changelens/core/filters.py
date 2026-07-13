import fnmatch
from pathlib import Path
from typing import List

def load_ignore_file_patterns(base_dir: Path) -> List[str]:
    """
    Looks for a .changelensignore file at the target root and parses its patterns,
    skipping comments and empty lines.
    """
    ignore_file = base_dir / ".changelensignore"
    if not ignore_file.is_file():
        return []
        
    patterns = []
    try:
        with open(ignore_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                patterns.append(line)
    except Exception:
        # Fallback gracefully if the file is locked or unreadable
        return []
        
    return patterns

def is_excluded(file_path: Path, base_dir: Path, exclude_patterns: List[str]) -> bool:
    """
    Checks if a file matches any of the provided exclusion glob patterns.
    """
    if not exclude_patterns:
        return False
        
    rel_path = file_path.relative_to(base_dir).as_posix()
    
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(file_path.name, pattern) or fnmatch.fnmatch(rel_path, pattern):
            return True
            
    return False