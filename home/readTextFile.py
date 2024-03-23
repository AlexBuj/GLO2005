def read_file(path):
    file = open(path, 'r')
    return file.read().split('\n')