from core.snapshot import get_files_in_directory
from core.hasher import generate_snapshot_dict

def run_cli():
    directory = input("Enter directory path to scan: ")

    try:
        # Step 1: Discover all files
        found_files = get_files_in_directory(directory)
        print(f"Found {len(found_files)} files. Calculating hashes...")
        
        # Step 2: Generate the hash dictionary
        hash_dict = generate_snapshot_dict(directory, found_files)
        
        # Step 3: Output the results
        print(f"\n--- Scan Results ---")
        for rel_path, file_hash in hash_dict.items():
            print(f"{rel_path}: {file_hash}")
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except NotADirectoryError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_cli()