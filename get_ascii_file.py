import os
import chardet

def check_ascii_files(directory_path, output_file):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                contents = f.read()
                encoding = chardet.detect(contents)['encoding']
                if encoding == 'ascii':
                    output_file.write(file_path + '\n')

# Example usage
directory_path =  'C:/TFS/Practice/DPROG'
output_file_path = 'C:/TFS/output.txt'
with open(output_file_path, 'w') as output_file:
    check_ascii_files(directory_path, output_file)


def get_Count(path):
    cd_count = sess.run_ps("Set-Location "+path)
    counts = {}
    extensions = [".exe", ".dll", ".bin",".txt",".cs"]
    for ext in extensions:
        result_count = sess.run_ps("Get-ChildItem "+path+" -Recurse | Where-Object {$_.Extension -eq '"+ext+"'}")
        directories_count = result_count.std_out.splitlines()
        count = 0
        for directory_count in directories_count[3:]:
            if len(directory_count) > 0:
                count += 1
        counts[ext] = count
    for ext, count in counts.items():
        write_to_file(f"{ext} count = {count}")
    write_to_file("")


# import os
# import chardet

# def is_ascii(filename):
#     with open(filename, 'rb') as f:
#         result = chardet.detect(f.read())
#         return result['encoding'] == 'ascii'

# def find_ascii_files(directory):
#     ascii_files = []
#     for root, _, files in os.walk(directory):
#         for file in files:
#             if is_ascii(os.path.join(root, file)):
#                 ascii_files.append(os.path.join(root, file))
#     return ascii_files


# import os

# def is_ascii(file_path):
    # try:
    #     with open(file_path, 'rb') as f:
    #         content = f.read()
    #         content.decode('ascii')
    #         return True
    # except UnicodeDecodeError:
    #     return False


#     filename = file_path
#     # with open(filename) as f:
#     with open(filename, encoding='latin-1') as f:
#         content = f.readlines()
#         for entry in content:
#             try:
#                 entry.encode('ascii', errors='ignore').decode('ascii')
#             except UnicodeDecodeError:
#                 print(file_path+" it was not an ASCII-encoded Unicode string")
#             else:
#                 print(file_path+" It may have been an ASCII-encoded Unicode string")
#             f.close()
    

# def print_ascii_files(path):
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             if is_ascii(file_path):
#                 print(file_path)

# # Replace 'path/to/project' with the path to your project directory
# print_ascii_files('C:/TFS/Practice/DPROG')


