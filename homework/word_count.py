"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
import time
from itertools import groupby

from toolz.itertoolz import concat, pluck


def copy_raw_files_to_input_folder(n):
    """Generate n copies of the raw files in the input folder"""
    input_dir = "files/input"
    os.makedirs(input_dir, exist_ok=True)

    # Clean existing files in input folder
    for f in glob.glob(os.path.join(input_dir, "*")):
        os.remove(f)

    raw_files = glob.glob("files/raw/*")

    for i in range(n):
        for raw_file in raw_files:
            basename = os.path.basename(raw_file)
            name, ext = os.path.splitext(basename)
            dest = os.path.join(input_dir, f"{name}_copy{i}{ext}")
            with open(raw_file, "r", encoding="utf-8") as src:
                content = src.read()
            with open(dest, "w", encoding="utf-8") as dst:
                dst.write(content)


def load_input(input_directory):
    """Funcion load_input"""
    files = glob.glob(os.path.join(input_directory, "*"))
    sequence = fileinput.input(files=files)
    return sequence


def preprocess_line(x):
    """Preprocess the line x"""
    x = x.strip()
    x = x.lower()
    x = x.replace(",", "")
    x = x.replace(".", "")
    x = x.replace("(", "")
    x = x.replace(")", "")
    return x


def map_line(x):
    preprocessed = preprocess_line(x)
    words = preprocessed.split()
    return [(word, 1) for word in words]


def mapper(sequence):
    """Mapper"""
    mapped = [map_line(line) for line in sequence]
    return list(concat(mapped))


def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    sequence = sorted(sequence, key=lambda x: x[0])
    return sequence


def compute_sum_by_group(group):
    key, values = group
    total = sum(pluck(1, values))
    return (key, total)


def reducer(sequence):
    """Reducer"""
    groups = groupby(sequence, key=lambda x: x[0])
    result = [compute_sum_by_group((key, list(group))) for key, group in groups]
    return result


def create_directory(directory):
    """Create Output Directory"""
    os.makedirs(directory, exist_ok=True)


def save_output(output_directory, sequence):
    """Save Output"""
    with open(os.path.join(output_directory, "part-00000"), "w", encoding="utf-8") as f:
        for key, value in sequence:
            f.write(f"{key}\t{value}\n")


def create_marker(output_directory):
    """Create Marker"""
    with open(os.path.join(output_directory, "_SUCCESS"), "w", encoding="utf-8") as f:
        f.write("")


def run_job(input_directory, output_directory):
    """Job"""
    sequence = load_input(input_directory)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)


if __name__ == "__main__":

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
