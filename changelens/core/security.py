import hmac
import hashlib
import json
from typing import Dict, Any

def compute_signature(snapshot_data: Dict[str, Any], secret_key: str) -> str:
    """
    Computes an HMAC-SHA256 signature over normalized snapshot data.
    Keys are sorted and compact separators are enforced to guarantee 
    deterministic serialization signatures.
    """
    # Exclude any existing signature from the computation structure
    normalized_data = {k: v for k, v in snapshot_data.items() if k != "signature"}
    serialized = json.dumps(normalized_data, sort_keys=True, separators=(',', ':'))
    
    return hmac.new(
        secret_key.encode('utf-8'),
        serialized.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()