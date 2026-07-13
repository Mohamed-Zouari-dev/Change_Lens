from pathlib import Path
from typing import Dict, List
import hashlib
from concurrent.futures import ThreadPoolExecutor

def hash_file(file_path: Path) -> str:
    """
    Computes the SHA-256 hash of a file safely using stream chunking.
    Returns an empty string if the file is inaccessible.
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):  # Optimized 64KB block size for I/O efficiency
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError):
        return ""

def _hash_worker(args) -> tuple:
    """Worker task mapping an absolute file path to its relative path dict entry."""
    target_path, file_path = args
    file_hash = hash_file(file_path)
    if file_hash:
        rel_path = str(file_path.relative_to(target_path))
        return rel_path, {"hash": file_hash}
    return None

def generate_file_states(target_dir: str, files: List[Path]) -> Dict[str, dict]:
    """
    Generates cryptographic file states concurrently using a worker pool.
    Drastically speeds up performance over deep/large directory structures.
    """
    target = Path(target_dir)
    file_states = {}
    
    # Pack arguments for the thread workers
    worker_tasks = [(target, file) for file in files]
    
    # Process tasks concurrently to maximize I/O throughput
    with ThreadPoolExecutor() as executor:
        results = executor.map(_hash_worker, worker_tasks)
        
    for result in results:
        if result:
            rel_path, state_data = result
            file_states[rel_path] = state_data
            
    return file_states