# import os

# def list_files(directory,output_file):
#     """
#     This function lists all files in the given directory recursively.
#     """
#     file_list = []

#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             file_list.append(os.path.join(root, file))
#     save_to_txt(file_list, output_file)

# def save_to_txt(file_list, output_file):
#     """
#     This function saves the given list of files to a text file.
#     """
#     with open(output_file, 'w') as f:
#         f.write(f"Total files: {len(file_list)}\n\n")
#         for file in file_list:
#             f.write(file + '\n')
#     print(f"List of files saved in {output_file}")


import os

import os

def list_files(directory, output_file):
    """
    This function lists all files in the given directory recursively and writes the output to a file.
    """
    file_count = 0
    folder_count = 0

    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            file_count += len(files)
            folder_count += len(dirs)

        f.write(f"Total folders: {folder_count}\n")
        f.write(f"Total files: {file_count}\n")




