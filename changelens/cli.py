from core.hasher import hash_file

def run_cli():
    file_path = input("Enter file path: ")

    try:
        print(hash_file(file_path))
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    run_cli()