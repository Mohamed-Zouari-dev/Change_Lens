from core.generator import create_snapshot_model
from storage.json_store import save_snapshot

def run_cli():
    # Gather user inputs
    directory = input("Enter directory path to scan: ")
    output_file = input("Enter output snapshot filename (e.g., my_snapshot.json): ")

    try:
        print(f"\nScanning '{directory}'...")
        
        # 1. Generate the snapshot data model
        snapshot = create_snapshot_model(directory)
        
        # 2. Persist to disk
        save_snapshot(snapshot, output_file)
        
        # 3. Feedback
        total = snapshot["metadata"]["total_files"]
        print(f"Success! Snapshot saved to '{output_file}'.")
        print(f"Successfully tracked {total} files.")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except NotADirectoryError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_cli()