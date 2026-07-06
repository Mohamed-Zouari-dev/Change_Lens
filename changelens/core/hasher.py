import hashlib



def hash_file(file_path: str) -> str:
    
    hash_func = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()
