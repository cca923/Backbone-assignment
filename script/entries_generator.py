import pandas as pd
from datetime import datetime
import os
import re


def get_project_root():
    try:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        return os.path.dirname(os.getcwd())


def generate_accounting_entries(file_path, target_month):
    try:
        # Load Excel with openpyxl (required for .xlsx)
        df = pd.read_excel(
            file_path, sheet_name="Schedule", header=2, engine="openpyxl"
        )
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

    # Reshape format
    amortization_cols = df.columns[3:-1]
    df_long = df.melt(
        id_vars=["Items", "Invoice number", "Invoice amount"],
        value_vars=amortization_cols,
        var_name="Date",
        value_name="Amount",
    )

    # Clean and filter the data
    df_long["Date"] = pd.to_datetime(
        df_long["Date"], errors="coerce"
    ) + pd.offsets.MonthEnd(0)
    df_long = df_long.dropna(subset=["Date", "Amount"])
    df_target = df_long[df_long["Date"].dt.to_period("M") == target_month]

    def generate_entries(row):
        date_str = row["Date"].strftime("%d/%m/%Y")
        description = f"Prepayment amortisation for {row['Items']}"
        reference = str(row["Invoice number"])
        amount = round(row["Amount"], 2)

        return [
            {
                "Date": date_str,
                "Description": description,
                "Reference": reference,
                "Account": "EXP001",
                "Amount": amount,
            },
            {
                "Date": date_str,
                "Description": description,
                "Reference": reference,
                "Account": "PRE001",
                "Amount": -amount,
            },
        ]

    entries = [
        entry for _, row in df_target.iterrows() for entry in generate_entries(row)
    ]
    return pd.DataFrame(entries)


if __name__ == "__main__":
    while True:
        target_month = input(
            "Enter target month in YYYY-MM format (e.g. 2024-05): "
        ).strip()
        if re.fullmatch(r"\d{4}-\d{2}", target_month):
            break
        print("Invalid format. Please enter the correct format.")

    # Set up paths
    project_root = get_project_root()
    input_path = os.path.join(project_root, "data", "Prepayment assignment.xlsx")
    output_dir = os.path.join(project_root, "output")

    month_str = pd.Period(target_month).strftime("%b%Y")
    output_filename = f"accounting_entries_{month_str}.csv"
    output_path = os.path.join(output_dir, output_filename)

    os.makedirs(output_dir, exist_ok=True)

    df = generate_accounting_entries(input_path, target_month)
    if df is not None:
        df.to_csv(output_path, index=False)
        print(f"File saved to: {output_path}")
