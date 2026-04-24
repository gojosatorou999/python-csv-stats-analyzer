# Python CSV Analyzer

A nice lightweight, dependency-free Python tool to analyze CSV files and generate statistical reports.

## Features

- **Row & Column Counting**: Get instant feedback on dataset size.
- **Type Inference**: Automatically detects if a column is numeric (`int`, `float`) or categorical (`str`).
- **Numeric Statistics**: Calculates Min, Max, Mean, Median, and Sum for numeric columns.
- **Categorical Insights**: Shows unique value counts and the top 3 most frequent entries.
- **Null Detection**: Tracks missing values per column.

## How It Works (Parsing Explanation

The core logic of this analyzer relies on Python's built-in `csv` module, specifically the `csv.DictReader`.

### The Parsing Process:
1. **File Access**: The script opens the file using a context manager (`with open(...)`) to ensure proper resource handling.
2. **Dictionary Mapping**: `DictReader` maps the first row of the CSV (headers) as keys for every subsequent row. This allows us to access data like `row['salary']` instead of index-based access like `row[4]`.
3. **Lazy Loading vs Memory**: In this implementation, we convert the reader object to a `list(reader)`. For very large files (GBs), a row-by-row streaming approach would be better, but for standard datasets, this provides faster lookups and easier analysis.
4. **Type Casting**: Since CSVs are text-based, everything is initially a string. The `_infer_type` method tries to cast values into `int` then `float`. If both fail, it defaults to `str`.

## Usage

Simply run the script and provide the path to your CSV file:

```bash
python analyzer.py your_data.csv
```

### Example Output

```text
==================================================
CSV ANALYSIS REPORT: data.csv
==================================================
Total Rows:    10
Total Columns: 5
--------------------------------------------------
Column: department
  Type:  str
  Count: 10 (Nulls: 0)
  Unique:   3
  Top 3:    'Engineering' (4), 'Sales' (3), 'Marketing' (3)
------------------------------
Column: salary
  Type:  int
  Count: 10 (Nulls: 0)
  Min/Max:  58000.0 / 120000.0
  Mean:     87100.0
  Sum:      871000.0
------------------------------
```

## Requirements

- Python 3.6+
- No external libraries required!
