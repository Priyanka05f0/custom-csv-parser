"""
benchmark.py

Generate a synthetic CSV dataset and compare the performance of
CustomCsvReader/CustomCsvWriter with Python's built-in csv module.
"""

import csv
import random
import string
import time
from pathlib import Path

from custom_csv import CustomCsvReader, CustomCsvWriter


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

BASELINE_FILE = DATA_DIR / "baseline_10000x5.csv"
CUSTOM_WRITE_FILE = DATA_DIR / "custom_written.csv"
CSV_WRITE_FILE = DATA_DIR / "csv_written.csv"


def random_field():
    """Generate a random field containing letters and sometimes commas, quotes or newlines."""
    length = random.randint(5, 20)
    letters = string.ascii_letters

    text = "".join(random.choice(letters) for _ in range(length))

    # Occasionally add special characters to test edge cases
    if random.random() < 0.2:
        text += ","
    if random.random() < 0.1:
        text += '"'
    if random.random() < 0.1:
        text += "\n" + "".join(random.choice(letters) for _ in range(5))

    return text


def generate_dataset(rows=10000, cols=5):
    """Return a list of lists representing random CSV data."""
    return [[random_field() for _ in range(cols)] for _ in range(rows)]


def write_baseline_csv():
    """Create a baseline CSV file using the built-in csv.writer."""
    if BASELINE_FILE.exists():
        return

    data = generate_dataset()
    with BASELINE_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def benchmark_reader(iterations=3):
    """Compare CustomCsvReader vs csv.reader."""
    custom_times = []
    csv_times = []

    for _ in range(iterations):
        # Custom reader
        start = time.perf_counter()
        with BASELINE_FILE.open("r", encoding="utf-8", newline="") as f:
            reader = CustomCsvReader(f)
            for _ in reader:
                pass
        custom_times.append(time.perf_counter() - start)

        # Built-in csv.reader
        start = time.perf_counter()
        with BASELINE_FILE.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            for _ in reader:
                pass
        csv_times.append(time.perf_counter() - start)

    print("Reader benchmark ({} runs):".format(iterations))
    print(f"  CustomCsvReader average: {sum(custom_times) / len(custom_times):.4f} s")
    print(f"  csv.reader     average: {sum(csv_times) / len(csv_times):.4f} s")
    print()


def benchmark_writer(iterations=3):
    """Compare CustomCsvWriter vs csv.writer."""
    data = generate_dataset()

    custom_times = []
    csv_times = []

    for _ in range(iterations):
        # Custom writer
        start = time.perf_counter()
        with CUSTOM_WRITE_FILE.open("w", encoding="utf-8", newline="") as f:
            writer = CustomCsvWriter(f)
            writer.write_rows(data)
        custom_times.append(time.perf_counter() - start)

        # Built-in csv.writer
        start = time.perf_counter()
        with CSV_WRITE_FILE.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        csv_times.append(time.perf_counter() - start)

    print("Writer benchmark ({} runs):".format(iterations))
    print(f"  CustomCsvWriter average: {sum(custom_times) / len(custom_times):.4f} s")
    print(f"  csv.writer      average: {sum(csv_times) / len(csv_times):.4f} s")
    print()


def main():
    write_baseline_csv()
    benchmark_reader()
    benchmark_writer()


if __name__ == "__main__":
    main()
