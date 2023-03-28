import os
           
def find_files_with_extension(root_directory, extensions):
    output_file= "C:\\Final_Script\\list_of_file.txt"
    with open(output_file, 'w') as f:
        f.write("File to be migrated to tfs:" + '\n')
        for dirpath, dirnames, filenames in os.walk(root_directory):
            for filename in filenames:
                for extension in extensions:
                    if filename.endswith(extension):
                        file_path = os.path.join(dirpath, filename)
                        f.write(file_path + '\n')