import json
import hmac
from typing import Dict, Any

def save_snapshot(snapshot: Dict[str, Any], filepath: str, secret_key: str = None) -> None:
    """
    Saves a snapshot dictionary to disk. Appends a tamper-proof 
    cryptographic signature if a secret key is supplied.
    """
    out_data = dict(snapshot)
    if secret_key:
        from changelens.core.security import compute_signature
        out_data["signature"] = compute_signature(out_data, secret_key)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=4)

def load_snapshot(filepath: str, secret_key: str = None) -> Dict[str, Any]:
    """
    Loads a snapshot file from disk and performs signature verification 
    if a tracking protection key is active.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if secret_key:
        from changelens.core.security import compute_signature
        if "signature" not in data:
            raise ValueError("Security Violation: Target snapshot file lacks an authenticity signature.")
        
        stored_signature = data["signature"]
        expected_signature = compute_signature(data, secret_key)
        
        # Constant-time verification loop prevents signature extraction via execution timing variance
        if not hmac.compare_digest(stored_signature, expected_signature):
            raise ValueError("CRITICAL SECURITY ALERT: The baseline snapshot file has been tampered with or modified!")

    return data