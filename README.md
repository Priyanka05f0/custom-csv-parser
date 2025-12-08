# Custom CSV Parser in Python

## 1. Project Overview

This project implements a simple CSV (Comma-Separated Values) reader and writer from scratch in Python, without using the built-in `csv` module for parsing and writing.

The goal is to understand:

- How CSV parsing works internally (handling commas, quotes, and newlines).
- How to design clean, iterator-based classes in Python.
- How to benchmark a custom implementation against the standard library.

The main classes are:

- `CustomCsvReader` – a streaming CSV reader implemented as an iterator.
- `CustomCsvWriter` – a CSV writer that correctly escapes and quotes fields.

---

## 2. Setup Instructions

### Prerequisites

- Python 3.8 or higher installed.

### (Optional) Create and activate a virtual environment

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
