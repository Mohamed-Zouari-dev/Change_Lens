from core.verifier import verify_live_directory
from storage.json_store import load_snapshot

def handle_verify_integrity():
    snapshot_file = input("Enter the path to the stored snapshot JSON: ").strip()
    directory = input("Enter the directory path to verify: ").strip()
    
    try:
        stored_snapshot = load_snapshot(snapshot_file)
        
        # This now returns our structured IntegrityReport object
        report = verify_live_directory(stored_snapshot, directory)
        
        print("\n================ INTEGRITY REPORT ================")
        print(f"Report ID:             {report.audit_metadata.report_id}")
        print(f"Status:                {report.audit_metadata.status}")
        print(f"Base Snapshot Time:    {report.audit_metadata.base_snapshot_time}")
        print(f"Verification Run Time: {report.audit_metadata.verification_time}")
        print("--------------------------------------------------")
        
        if report.summary.is_clean:
            print(f" Success: System state perfectly matches baseline.")
            print(f"   ({report.summary.files_matched} files verified)")
            print("==================================================")
            return

        if report.changes.modified:
            print(f"\nMODIFIED FILES ({report.summary.files_modified}):")
            for file in report.changes.modified:
                print(f"  - {file.path}")
                print(f"    [Old]: {file.old_hash[:16]}...")
                print(f"    [New]: {file.new_hash[:16]}...")
                
        if report.changes.added:
            print(f"\n ++ ADDED FILES ({report.summary.files_added}):")
            for file in report.changes.added:
                print(f"  - {file.path} (Hash: {file.current_hash[:16]}...)")
                
        if report.changes.deleted:
            print(f"\n -- DELETED FILES ({report.summary.files_deleted}):")
            for file in report.changes.deleted:
                print(f"  - {file.path} (Last Hash: {file.last_known_hash[:16]}...)")
                
        print("==================================================")
        
    except FileNotFoundError:
        print(f"Error: Snapshot file '{snapshot_file}' could not be located.")