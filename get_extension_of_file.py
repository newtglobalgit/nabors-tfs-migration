import os
import csv

# dictionary to store the filenames with each extension
extension_files = {}

extension_counts = {}

# list to store the files without any extension
no_extension_files = []


def get_file_extension_details()
input_file = input("Enter the input file name: ")
with open(input_file, "r") as file:
    for line in file:

        extension = os.path.splitext(line.strip())[1]
 
        if extension:
            if extension in extension_files:
                extension_files[extension].append(line.strip())
                extension_counts[extension] += 1
            else:
                extension_files[extension] = [line.strip()]
                extension_counts[extension] = 1
        else:
            no_extension_files.append(line.strip())


output_file = "File_Extension.txt"
with open(output_file, "w") as file:
    file.write("Files grouped by extension:\n")
    for extension, files in extension_files.items():
        file.write(f"{extension}:\n")
        for f in files:
            file.write(f"\t{f}\n")
   
    file.write("Extension counts:\n")
    for extension, count in extension_counts.items():
        file.write(f"\t{extension}: {count}\n")

    if no_extension_files:
        file.write("Files Ignored:\n")
        for f in no_extension_files:
            file.write(f"\t{f}\n")