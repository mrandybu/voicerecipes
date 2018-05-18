import os

def get_root_path_to_file(filename):
    root_path = os.path.dirname(__file__)
    path_to_file = os.path.join(root_path, filename)
    return path_to_file