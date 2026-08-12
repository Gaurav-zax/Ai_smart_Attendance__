import tkinter as tk
from tkinter import messagebox
import csv
import os
import cv2
import sqlite3


# ==================================================
# PROJECT PATH
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==================================================
# FILES AND FOLDERS
# ==================================================

CSV_FILE = os.path.join(
    BASE_DIR,
    "students.csv"
)


DATABASE = os.path.join(
    BASE_DIR,
    "attendance.db"
)


DATASET_FOLDER = os.path.join(
    BASE_DIR,
    "dataset"
)


CASCADE_FILE = os.path.join(
    BASE_DIR,
    "haarcascade_frontalface_default.xml"
)


os.makedirs(
    DATASET_FOLDER,
    exist_ok=True
)


# ==================================================
# CREATE CSV IF NOT EXISTS
# ==================================================

if not os.path.exists(CSV_FILE):

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Student_ID",
                "Student_Name"
            ]
        )


# ==================================================
# DATABASE
# ==================================================

def connect_db():

    return sqlite3.connect(
        DATABASE
    )


# ==================================================
# REGISTER STUDENT
# ==================================================

def register_student():

    student_id_text = id_entry.get().strip()

    student_name = name_entry.get().strip()


    # ----------------------------------------------
    # VALIDATE ID
    # ----------------------------------------------

    if not student_id_text.isdigit():

        messagebox.showerror(
            "Invalid Student ID",
            "Student ID must contain numbers only."
        )

        return


    student_id = int(
        student_id_text
    )


    # ----------------------------------------------
    # VALIDATE NAME
    # ----------------------------------------------

    if student_name == "":

        messagebox.showerror(
            "Invalid Name",
            "Student Name cannot be empty."
        )

        return


    # ----------------------------------------------
    # CHECK DUPLICATE ID
    # ----------------------------------------------

    conn = connect_db()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT student_name
        FROM students
        WHERE student_id = ?
        """,

        (
            student_id,
        )
    )


    existing_student = cursor.fetchone()


    conn.close()


    if existing_student is not None:

        messagebox.showerror(
            "Student ID Already Exists",

            f"Student ID {student_id} is already registered."
        )

        return


    # ----------------------------------------------
    # SAVE TO CSV
    # ----------------------------------------------

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                student_id,
                student_name
            ]
        )


    # ----------------------------------------------
    # SAVE TO SQLITE
    # ----------------------------------------------

    conn = connect_db()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO students
        (
            student_id,
            student_name
        )

        VALUES (?, ?)
        """,

        (
            student_id,
            student_name
        )
    )


    conn.commit()

    conn.close()


    messagebox.showinfo(
        "Success",
        "Student details saved successfully.\n\n"
        "Now the camera will open for face registration."
    )


    window.destroy()


    start_camera(
        student_id
    )


# ==================================================
# START CAMERA
# ==================================================

def start_camera(student_id):

    face_detector = cv2.CascadeClassifier(
        CASCADE_FILE
    )


    if face_detector.empty():

        messagebox.showerror(
            "Error",
            "Haar Cascade file not found!"
        )

        return


    camera = cv2.VideoCapture(
        0
    )


    if not camera.isOpened():

        messagebox.showerror(
            "Camera Error",
            "Camera could not be opened."
        )

        return


    count = 0


    print(
        "Opening Registration Camera..."
    )


    while True:

        ret, frame = camera.read()


        if not ret:

            print(
                "Camera Error!"
            )

            break


        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )


        faces = face_detector.detectMultiScale(
            gray,

            1.3,

            5
        )


        for (x, y, w, h) in faces:


            cv2.rectangle(
                frame,

                (x, y),

                (x + w, y + h),

                (0, 255, 0),

                2
            )


            count += 1


            image_path = os.path.join(
                DATASET_FOLDER,

                f"User.{student_id}.{count}.jpg"
            )


            cv2.imwrite(
                image_path,

                gray[
                    y:y + h,

                    x:x + w
                ]
            )


            cv2.putText(
                frame,

                f"Images: {count}/100",

                (x, y - 10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (0, 255, 0),

                2
            )


        cv2.imshow(
            "Student Registration Camera",

            frame
        )


        if count >= 100:

            print(
                "100 Images Captured Successfully!"
            )

            break


        if cv2.waitKey(1) & 0xFF == ord("q"):

            print(
                "Registration stopped by user."
            )

            break


    camera.release()


    cv2.destroyAllWindows()


# ==================================================
# REGISTRATION WINDOW
# ==================================================

window = tk.Tk()


window.title(
    "Register New Student"
)


window.geometry(
    "450x300"
)


window.resizable(
    False,

    False
)


# ==================================================
# TITLE
# ==================================================

title_label = tk.Label(

    window,

    text="REGISTER NEW STUDENT",

    font=(
        "Arial",

        20,

        "bold"
    )
)


title_label.pack(
    pady=20
)


# ==================================================
# STUDENT ID
# ==================================================

id_label = tk.Label(

    window,

    text="Student ID",

    font=(
        "Arial",

        12
    )
)


id_label.pack()


id_entry = tk.Entry(

    window,

    width=30,

    font=(
        "Arial",

        12
    )
)


id_entry.pack(
    pady=8
)


# ==================================================
# STUDENT NAME
# ==================================================

name_label = tk.Label(

    window,

    text="Student Name",

    font=(
        "Arial",

        12
    )
)


name_label.pack()


name_entry = tk.Entry(

    window,

    width=30,

    font=(
        "Arial",

        12
    )
)


name_entry.pack(
    pady=8
)


# ==================================================
# BUTTON
# ==================================================

register_button = tk.Button(

    window,

    text="Register Student",

    width=25,

    height=2,

    command=register_student
)


register_button.pack(
    pady=20
)


# ==================================================
# START
# ==================================================

id_entry.focus()


window.mainloop()