from changelens.core.hasher import hash_file

def run_cli():
    file_path = input("Enter file path: ")

    try:
        print(hash_file(file_path))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_cli()