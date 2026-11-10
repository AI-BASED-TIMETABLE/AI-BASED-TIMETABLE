AI-BASED TIMETABLE PROJECT - DATA FILES

Included:
1. AI_Based_Timetable_Dataset_1000_Records.xlsx - original dataset
2. data_cleaning.py - cleans the original Excel dataset
3. clean_dataset.csv - cleaned dataset
4. Data_analysis.py - produces analysis_summary.txt and CSV summaries
5. Data_visualisation.py - creates 8 different chart types
6. analysis_summary.txt and summary CSV files - generated analysis outputs
7. visualisations/ - all 8 generated chart images

Charts generated:
1. Pie chart - timetable status distribution
2. Donut chart - AI recommendation distribution
3. Line graph - timetable records by day
4. Histogram - student count distribution
5. Box plot - student count by department
6. Scatter plot - student count vs room capacity
7. Stacked bar chart - valid vs rescheduled records by department
8. Heatmap - department-wise timetable distribution by day

How to run:
1. Install Python 3.
2. Open a terminal in this folder.
3. Install required libraries:
   pip install pandas openpyxl matplotlib
4. Run:
   python data_cleaning.py
   python Data_analysis.py
   python Data_visualisation.py

Note: Project Proposal and Power BI (.pbix) dashboard are intentionally excluded.
