import os

def list_files(directory, output_file):
    file_count = 0
    folder_count = 0

    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            file_count += len(files)
            folder_count += len(dirs)

        f.write(f"Total folders: {folder_count}\n")
        f.write(f"Total files: {file_count}\n")