from changelens.core.hasher import hash_file


def run_cli():
    file_path = input("Enter the file path to hash: ")
    try :
        file_hash = hash_file(file_path)
        print(f"hash of '{file_path}': {file_hash}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    

