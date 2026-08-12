import csv
import os
from database import connect_db

FILE_NAME = "students.csv"

print("=" * 50)
print("Current Folder :", os.getcwd())
print("CSV File Exists :", os.path.exists(FILE_NAME))
print("=" * 50)

if not os.path.exists(FILE_NAME):
    print("ERROR: students.csv file not found!")
    exit()

# CSV content check
with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
    print("\nCSV File Content:\n")
    print(file.read())

conn = connect_db()
cursor = conn.cursor()

count = 0

with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    print("\nCSV Headers :", reader.fieldnames)

    for row in reader:

        print("Reading Row :", row)

        student_id = int(row["Student_ID"])
        student_name = row["Student_Name"]

        cursor.execute(
            """
            INSERT OR REPLACE INTO students
            (student_id, student_name)
            VALUES (?, ?)
            """,
            (student_id, student_name)
        )

        count += 1

conn.commit()
conn.close()

print("\nTotal Students Imported :", count)
print("Import Completed Successfully!")