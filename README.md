# Prepayment Accounting Entry Generator

This Python script automates the generation of accounting journal entries for amortized prepayments based on a monthly schedule from an Excel file.

---

## Dependencies

- Python 3.8+
- pandas
- openpyxl

### Install with:

```
pip install pandas openpyxl
```

---

## How to Use

### 1. Navigate to the `script/` folder:

```
cd script
```

### 2. Run the script:

```
python entries_generator.py
```

### 3. When prompted, enter the desired target month in YYYY-MM format:

```
Enter target month in YYYY-MM format (e.g. 2024-05): <input>
```

### 4. The result will be saved to the `output/` folder with a filename like:

```
accounting_entries_May2024.csv
```

---

## Input File Requirements

Your input Excel file (`Prepayment assignment.xlsx`) should:

- Be located in the `data/` directory
- Start from **Row 3** (`header=2`) where columns include:
  - `Items`, `Invoice number`, `Invoice amount`
  - Followed by monthly columns.

---

## What It Does

- Reshapes the Excel sheet from wide to long format.
- Filters the rows based on the target month.
- Generates two journal entries per item:
  - Debit to **EXP001** (expense)
  - Credit to **PRE001** (prepaid)
