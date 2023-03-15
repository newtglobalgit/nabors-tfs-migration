import os

def get_file_count(path):
    ascii_count = 0
    binary_count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt') or file.endswith('.py'):
                ascii_count += 1
            else:
                binary_count += 1
    return ascii_count, binary_count

if __name__ == '__main__':
    path = 'http://192.168.3.197:8080/tfs'
    ascii_count, binary_count = get_file_count(path)
    print('Number of ASCII files:', ascii_count)
    print('Number of binary files:', binary_count)