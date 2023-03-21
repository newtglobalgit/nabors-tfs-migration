# import os

# # dictionary to store the filenames with each extension
# extension_files = {}

# extension_counts = {}

# # list to store the files without any extension
# no_extension_files = []

# with open("C:\TFS\Demo\output_file.txt", "r") as file:
#     for line in file:

#         extension = os.path.splitext(line.strip())[1]
 
#         if extension:
#             if extension in extension_files:
#                 extension_files[extension].append(line.strip())
#                 extension_counts[extension] += 1
#             else:
#                 extension_files[extension] = [line.strip()]
#                 extension_counts[extension] = 1
#         else:
#             no_extension_files.append(line.strip())


# for extension, files in extension_files.items():
#     print(f"{extension}:")
#     for file in files:
#         print(f"\t{file}")
#     print()
        

# if no_extension_files:
#     print("Files without extension:")
#     for file in no_extension_files:
#         print(f"\t{file}")
#     print()

# for extension, count in extension_counts.items():
#     print(f"{extension}: {count}")
#     print()

import os
import csv

# dictionary to store the filenames with each extension
extension_files = {}

extension_counts = {}

# list to store the files without any extension
no_extension_files = []

with open("C:\TFS\Demo\output_file.txt", "r") as file:
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

# Write the output to a CSV file
with open("output.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the files grouped by extension
    for extension, files in extension_files.items():
        row = [extension] + files
        writer.writerow(row)
    
    # Write the files without an extension
    if no_extension_files:
        writer.writerow(["Files without extension:"])
        writer.writerow(no_extension_files)
    
    # Write the extension counts
    for extension, count in extension_counts.items():
        writer.writerow([extension, count])