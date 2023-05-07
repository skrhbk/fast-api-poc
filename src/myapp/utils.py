import pathlib


def get_sibling_file_path(file_path, rel_path):
    return f"{pathlib.Path(file_path).parent}/{rel_path}"
