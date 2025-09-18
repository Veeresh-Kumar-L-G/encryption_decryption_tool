import os

def read_file(file_path, mode="r"):
    with open(file_path, mode) as f:
        return f.read() if "b" not in mode else f.read()

def write_file(file_path, data, mode="w"):
    with open(file_path, mode) as f:
        f.write(data if isinstance(data, str) else data.decode(errors="ignore"))

def output_filename(file_path, suffix):
    base, ext = os.path.splitext(file_path)
    return f"{base}_{suffix}{ext}"
