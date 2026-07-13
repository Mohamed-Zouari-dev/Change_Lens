from core.generator import create_snapshot_model
from core.verifier import verify_live_directory
from storage.json_store import save_snapshot, load_snapshot

def handle_create_snapshot():
    directory = input("Enter directory path to scan: ").strip()
    output_file = input("Enter output snapshot filename (e.g., base.json): ").strip()
    
    print(f"\nScanning '{directory}'...")
    snapshot = create_snapshot_model(directory)
    save_snapshot(snapshot, output_file)
    print(f"Success! Snapshot saved to '{output_file}'.")

def handle_verify_integrity():
    snapshot_file = input("Enter the path to the stored snapshot JSON: ").strip()
    directory = input("Enter the directory path to verify: ").strip()
    
    try:
        stored_snapshot = load_snapshot(snapshot_file)
        diff = verify_live_directory(stored_snapshot, directory)
        
        summary = diff["summary"]
        
        print("\n================ INTEGRITY REPORT ================")
        print(f"Base Snapshot Time:    {summary['base_timestamp']}")
        print(f"Verification Run Time: {summary['current_timestamp']}")
        print("--------------------------------------------------")
        
        has_changes = (summary["added_count"] > 0 or 
                       summary["deleted_count"] > 0 or 
                       summary["modified_count"] > 0)
        
        if not has_changes:
            print("✅ Success: System state matches baseline perfectly.")
            print("==================================================")
            return

        if diff["modified"]:
            print(f"\n❌ MODIFIED FILES ({summary['modified_count']}):")
            for file in diff["modified"]:
                print(f"  - {file['path']}")
                print(f"    [Old]: {file['old_hash'][:16]}...")
                print(f"    [New]: {file['new_hash'][:16]}...")
                
        if diff["added"]:
            print(f"\n➕ ADDED FILES ({summary['added_count']}):")
            for file in diff["added"]:
                print(f"  - {file['path']} (Hash: {file['current_hash'][:16]}...)")
                
        if diff["deleted"]:
            print(f"\n🗑️  DELETED FILES ({summary['deleted_count']}):")
            for file in diff["deleted"]:
                print(f"  - {file['path']} (Last Hash: {file['last_known_hash'][:16]}...)")
                
        print("==================================================")
        
    except FileNotFoundError:
        print(f"Error: Snapshot file '{snapshot_file}' could not be located.")

def run_cli():
    print("ChangeLens File Integrity Monitor")
    print("1. Create New Snapshot")
    print("2. Verify Directory Integrity")
    choice = input("Select an option (1/2): ").strip()
    
    try:
        if choice == "1":
            handle_create_snapshot()
        elif choice == "2":
            handle_verify_integrity()
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"\nAn unexpected runtime error occurred: {e}")

if __name__ == "__main__":
    run_cli()