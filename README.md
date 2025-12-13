# Custom CSV Parser in Python

## 1. Project Overview

This project implements a custom CSV (Comma-Separated Values) **reader** and **writer** from scratch in Python, **without using the built-in `csv` module for parsing**.  
The main objective is to understand:

- Low-level CSV parsing (handling commas, quotes, escaped quotes, and embedded newlines)
- Iterators and streaming file processing
- Writing CSV files correctly with quoting and escaping rules
- Benchmarking performance against Python’s standard `csv` module

### Implemented Components

- **CustomCsvReader**  
  A streaming, iterator-based CSV parser that:
  - Reads files character-by-character  
  - Correctly handles quoted fields  
  - Decodes escaped quotes (`""`)  
  - Supports newline characters *inside* quoted fields  
  - Processes file in streaming mode (does not load entire file into memory)

- **CustomCsvWriter**  
  A CSV writer that:
  - Escapes existing quotes  
  - Automatically quotes fields containing commas, quotes, or newlines  
  - Writes valid CSV rows readable by any standard CSV parser

---

## 2. Setup Instructions

### Prerequisites
- **Python 3.8+** installed

### (Optional) Create and activate a virtual environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

