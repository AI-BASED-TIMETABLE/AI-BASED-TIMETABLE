
import os
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------
# CONFIGURATION
# -----------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(BASE_DIR, "clean_dataset.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "visualisations")

DAY_ORDER = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday"
]

REQUIRED_COLUMNS = [
    "Timetable_Status",
    "AI_Recommendation",
    "Day",
    "Student_Count",
    "Department",
    "Room_Capacity"
]


# -----------------------------------------
# SAVE CHART
# -----------------------------------------

def save_chart(filename):
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_DIR, filename)

    plt.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Generated: {filename}")


# -----------------------------------------
# MAIN FUNCTION
# -----------------------------------------

def main():

    # Create output folder
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Check CSV file
    if not os.path.exists(INPUT_FILE):
        print("ERROR: clean_dataset.csv not found!")
        print("Place the CSV file in the same folder as this Python script.")
        return

    # Read dataset
    try:
        df = pd.read_csv(INPUT_FILE)
    except Exception as e:
        print("Error reading CSV file:", e)
        return

    # Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        print("ERROR: Missing columns in CSV file:")
        print(missing_columns)
        print("Available columns:", list(df.columns))
        return

    if df.empty:
        print("ERROR: The CSV dataset is empty.")
        return

    # Clean data
    for col in [
        "Timetable_Status",
        "AI_Recommendation",
        "Day",
        "Department"
    ]:
        df[col] = df[col].astype("string").str.strip()

    df["Student_Count"] = pd.to_numeric(
        df["Student_Count"],
        errors="coerce"
    )

    df["Room_Capacity"] = pd.to_numeric(
        df["Room_Capacity"],
        errors="coerce"
    )

    # Normalize day names
    df["Day"] = df["Day"].str.capitalize()

    print("\nDataset loaded successfully!")
    print("Total records:", len(df))

    # =====================================
    # 1. PIE CHART
    # Timetable Status Distribution
    # =====================================

    status = df["Timetable_Status"].dropna().value_counts()

    if not status.empty:

        plt.figure(figsize=(7, 6))

        plt.pie(
            status.values,
            labels=status.index,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"edgecolor": "white"}
        )

        plt.title("Timetable Status Distribution")

        save_chart("01_timetable_status_pie.png")

    # =====================================
    # 2. DONUT CHART
    # AI Recommendation Distribution
    # =====================================

    recommendations = (
        df["AI_Recommendation"]
        .dropna()
        .value_counts()
    )

    if not recommendations.empty:

        plt.figure(figsize=(8, 6))

        plt.pie(
            recommendations.values,
            labels=recommendations.index,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={
                "width": 0.42,
                "edgecolor": "white"
            },
            pctdistance=0.78,
            labeldistance=1.08
        )

        plt.title("AI Recommendation Distribution")

        save_chart("02_ai_recommendations_donut.png")

    # =====================================
    # 3. LINE GRAPH
    # Timetable Records by Day
    # =====================================

    daily = (
        df["Day"]
        .value_counts()
        .reindex(DAY_ORDER, fill_value=0)
    )

    plt.figure(figsize=(9, 5))

    plt.plot(
        daily.index,
        daily.values,
        marker="o",
        linewidth=2
    )

    plt.title("Timetable Records by Day")
    plt.xlabel("Day")
    plt.ylabel("Number of Records")

    plt.grid(
        True,
        linestyle="--",
        alpha=0.4
    )

    plt.xticks(rotation=20)

    save_chart("03_records_by_day_line.png")

    # =====================================
    # 4. HISTOGRAM
    # Student Count Distribution
    # =====================================

    student_counts = df["Student_Count"].dropna()

    if not student_counts.empty:

        plt.figure(figsize=(8, 5))

        plt.hist(
            student_counts,
            bins=12,
            edgecolor="black"
        )

        plt.title("Student Count Distribution")
        plt.xlabel("Number of Students")
        plt.ylabel("Frequency")

        save_chart("04_student_count_histogram.png")

    # =====================================
    # 5. BOX PLOT
    # Student Count by Department
    # =====================================

    box_df = df.dropna(
        subset=["Department", "Student_Count"]
    )

    departments = sorted(
        box_df["Department"].unique()
    )

    if departments:

        box_data = [
            box_df.loc[
                box_df["Department"] == dept,
                "Student_Count"
            ].values
            for dept in departments
        ]

        plt.figure(figsize=(9, 5))

        plt.boxplot(
            box_data,
            patch_artist=True,
            showmeans=True
        )

        # Compatible with older Matplotlib versions
        plt.xticks(
            range(1, len(departments) + 1),
            departments
        )

        plt.title("Student Count by Department")
        plt.xlabel("Department")
        plt.ylabel("Number of Students")

        save_chart(
            "05_student_count_by_department_boxplot.png"
        )

    # =====================================
    # 6. SCATTER PLOT
    # Student Count vs Room Capacity
    # =====================================

    scatter_df = df.dropna(
        subset=["Room_Capacity", "Student_Count"]
    )

    if not scatter_df.empty:

        plt.figure(figsize=(8, 5))

        plt.scatter(
            scatter_df["Room_Capacity"],
            scatter_df["Student_Count"],
            alpha=0.6
        )

        plt.title(
            "Student Count vs Room Capacity"
        )

        plt.xlabel("Room Capacity")
        plt.ylabel("Student Count")

        plt.grid(
            True,
            linestyle="--",
            alpha=0.3
        )

        save_chart(
            "06_student_count_vs_room_capacity_scatter.png"
        )

    # =====================================
    # 7. STACKED BAR GRAPH
    # Department-wise Timetable Status
    # =====================================

    status_df = df.dropna(
        subset=["Department", "Timetable_Status"]
    )

    status_by_dept = pd.crosstab(
        status_df["Department"],
        status_df["Timetable_Status"]
    )

    status_by_dept = status_by_dept.reindex(
        columns=["Valid", "Needs Rescheduling"],
        fill_value=0
    )

    if not status_by_dept.empty:

        ax = status_by_dept.plot(
            kind="bar",
            stacked=True,
            figsize=(9, 5)
        )

        ax.set_title(
            "Valid vs Rescheduled Records by Department"
        )

        ax.set_xlabel("Department")
        ax.set_ylabel("Number of Records")

        ax.legend(
            title="Timetable Status"
        )

        plt.xticks(rotation=0)

        save_chart(
            "07_status_by_department_stacked_bar.png"
        )

    # =====================================
    # 8. HEATMAP
    # Department-wise Timetable Distribution
    # =====================================

    heat_df = df.dropna(
        subset=["Department", "Day"]
    )

    heat = pd.crosstab(
        heat_df["Department"],
        heat_df["Day"]
    ).reindex(
        columns=DAY_ORDER,
        fill_value=0
    )

    if not heat.empty:

        plt.figure(figsize=(10, 6))

        image = plt.imshow(
            heat.values,
            aspect="auto",
            cmap="YlOrRd"
        )

        plt.colorbar(
            image,
            label="Number of Records"
        )

        plt.xticks(
            range(len(heat.columns)),
            heat.columns,
            rotation=25,
            ha="right"
        )

        plt.yticks(
            range(len(heat.index)),
            heat.index
        )

        plt.title(
            "Department-wise Timetable Distribution (Heatmap)"
        )

        plt.xlabel("Day")
        plt.ylabel("Department")

        # Display values inside heatmap cells
        for row in range(heat.shape[0]):
            for col in range(heat.shape[1]):

                plt.text(
                    col,
                    row,
                    int(heat.iloc[row, col]),
                    ha="center",
                    va="center",
                    fontsize=8
                )

        save_chart(
            "08_department_day_heatmap.png"
        )

    # =====================================
    # FINAL OUTPUT
    # =====================================

    print("\n======================================")
    print(" TIMETABLE VISUALIZATION COMPLETED")
    print("======================================")

    print("Successfully generated available graph types.")
    print("Output folder:", OUTPUT_DIR)

    print("\nGenerated files:")

    for filename in sorted(os.listdir(OUTPUT_DIR)):
        if filename.endswith(".png"):
            print(" -", filename)


# =====================================
# PROGRAM ENTRY POINT
# =====================================

if __name__ == "__main__":
    main()
