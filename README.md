# AI-powered-finance-asssistent

## Pandas data cleaning program

This repository now includes a simple pandas-based data cleaning script:

- `pandas_data_cleaning.py`

### Usage

```bash
python pandas_data_cleaning.py input.csv output.csv
```

### What it does

- Standardizes column names.
- Removes duplicate rows.
- Trims extra whitespace in text columns.
- Attempts date parsing for columns like `date` or `*_at`.
- Converts numeric-like text to numbers when conversion is reliable.
- Fills missing numeric values with median.
- Fills missing text values with mode.
- Drops fully empty rows.
