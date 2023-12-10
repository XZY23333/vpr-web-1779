import os
import sys

def rename_files_in_subfolders(parent_dir):
    for subdir in os.listdir(parent_dir):
        subdir_path = os.path.join(parent_dir, subdir)
        if os.path.isdir(subdir_path):
            count = 1
            for filename in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, filename)
                if os.path.isfile(file_path):
                    new_filename = f"{subdir}_{count}{os.path.splitext(filename)[1]}"
                    new_file_path = os.path.join(subdir_path, new_filename)
                    os.rename(file_path, new_file_path)
                    print(f"Renamed '{file_path}' to '{new_file_path}'")
                    count += 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_directory>")
        sys.exit(1)

    parent_directory = sys.argv[1]
    if not os.path.exists(parent_directory) or not os.path.isdir(parent_directory):
        print("Invalid path!")
        sys.exit(1)

    rename_files_in_subfolders(parent_directory)
