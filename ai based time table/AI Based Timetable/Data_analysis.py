"""
Analyze the cleaned timetable dataset.
Run: python Data_analysis.py
Outputs: analysis_summary.txt and CSV summary tables.
"""
import pandas as pd

INPUT_FILE = "clean_dataset.csv"

def main():
    df = pd.read_csv(INPUT_FILE)
    lines = [
        "AI-BASED TIMETABLE DATA ANALYSIS",
        "=" * 38,
        f"Total records: {len(df)}",
        f"Total columns: {len(df.columns)}",
        f"Duplicate rows: {int(df.duplicated().sum())}",
        f"Missing cells: {int(df.isna().sum().sum())}",
        "",
        "RECORDS BY DEPARTMENT",
        df["Department"].value_counts().to_string(),
        "",
        "TIMETABLE STATUS",
        df["Timetable_Status"].value_counts().to_string(),
        "",
        "AI RECOMMENDATIONS",
        df["AI_Recommendation"].value_counts().to_string(),
        "",
        "CONFLICT SUMMARY",
    ]

    for col in ["Faculty_Conflict", "Room_Conflict", "Conflict_Flag"]:
        if col in df.columns:
            lines.append(f"{col}:\n{df[col].value_counts().to_string()}")

    if "Student_Count" in df.columns:
        lines += [
            "",
            "STUDENT COUNT STATISTICS",
            df["Student_Count"].describe().round(2).to_string(),
        ]

    with open("analysis_summary.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    df["Department"].value_counts().rename_axis("Department").reset_index(
        name="Records"
    ).to_csv("department_summary.csv", index=False)
    df["Timetable_Status"].value_counts().rename_axis("Timetable_Status").reset_index(
        name="Records"
    ).to_csv("status_summary.csv", index=False)
    df["AI_Recommendation"].value_counts().rename_axis("AI_Recommendation").reset_index(
        name="Records"
    ).to_csv("recommendation_summary.csv", index=False)

    print("\n".join(lines))
    print("\nAnalysis files have been created.")

if __name__ == "__main__":
    main()
