"""
Clean the AI-Based Timetable dataset.
Run: python data_cleaning.py
Input : AI_Based_Timetable_Dataset_1000_Records.xlsx
Output: clean_dataset.csv
"""
import pandas as pd

INPUT_FILE = "AI_Based_Timetable_Dataset_1000_Records.xlsx"
OUTPUT_FILE = "clean_dataset.csv"

def clean_data():
    df = pd.read_excel(INPUT_FILE)

    # Remove leading/trailing spaces from column names and text values
    df.columns = df.columns.str.strip()
    text_columns = df.select_dtypes(include=["object"]).columns
    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # Replace empty text values with missing values
    df.replace(r"^\s*$", pd.NA, regex=True, inplace=True)

    # Remove duplicate rows and duplicate record IDs (keep first occurrence)
    df.drop_duplicates(inplace=True)
    if "Record_ID" in df.columns:
        df.drop_duplicates(subset=["Record_ID"], keep="first", inplace=True)

    # Fill missing numeric values with the column median
    numeric_columns = df.select_dtypes(include="number").columns
    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    # Fill missing text values with the most frequent value, or "Unknown"
    for column in text_columns:
        if df[column].isna().any():
            mode = df[column].mode(dropna=True)
            fill_value = mode.iloc[0] if not mode.empty else "Unknown"
            df[column] = df[column].fillna(fill_value)

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Cleaning completed. Saved {len(df)} records to {OUTPUT_FILE}")
    print("Missing values remaining:", int(df.isna().sum().sum()))

if __name__ == "__main__":
    clean_data()
