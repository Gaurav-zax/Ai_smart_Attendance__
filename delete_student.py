import sqlite3
import csv
import os
import glob


DATABASE = "attendance.db"



# Student ID input

student_id = input(
    "Enter Student ID to Delete: "
)





# Database delete

conn = sqlite3.connect(
    DATABASE
)

cursor = conn.cursor()



# Check student

cursor.execute(
    "SELECT * FROM students WHERE student_id=?",
    (student_id,)
)


student = cursor.fetchone()



if student is None:

    print(
        "Student not found!"
    )

    conn.close()

    exit()





# Delete from students table

cursor.execute(
    """
    DELETE FROM students
    WHERE student_id=?
    """,
    (student_id,)
)





# Delete attendance records

cursor.execute(
    """
    DELETE FROM attendance
    WHERE student_id=?
    """,
    (student_id,)
)





conn.commit()

conn.close()





# Remove from students.csv

if os.path.exists("students.csv"):


    rows=[]


    with open(
        "students.csv",
        "r"
    ) as file:


        reader=csv.reader(file)


        for row in reader:


            if len(row)>0 and row[0] != str(student_id):

                rows.append(row)





    with open(
        "students.csv",
        "w",
        newline=""
    ) as file:


        writer=csv.writer(file)

        writer.writerows(rows)







# Delete face images

images = glob.glob(
    f"dataset/User.{student_id}.*.jpg"
)


for image in images:

    os.remove(image)





print(
    "Student Deleted Successfully!"
)

print(
    "Now run train.py again to update AI model."
)