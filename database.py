import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sqlite3
import csv
from datetime import datetime
import os
import sys


# ==================================================
# PROJECT PATH
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==================================================
# FILE PATHS
# ==================================================

DATABASE = os.path.join(
    BASE_DIR,
    "attendance.db"
)

CSV_FILE = os.path.join(
    BASE_DIR,
    "students.csv"
)

DATASET_FOLDER = os.path.join(
    BASE_DIR,
    "dataset"
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "Attendance_Reports"
)


# ==================================================
# REQUIRED FOLDERS
# ==================================================

os.makedirs(
    DATASET_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# ==================================================
# DATABASE CONNECTION
# ==================================================

def connect_db():

    return sqlite3.connect(
        DATABASE
    )


# ==================================================
# INITIALIZE DATABASE
# ==================================================

def initialize_database():

    conn = connect_db()

    cursor = conn.cursor()


    # STUDENTS TABLE

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students
        (
            student_id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL
        )
        """
    )


    # ATTENDANCE TABLE

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            student_id INTEGER NOT NULL,
            student_name TEXT NOT NULL
        )
        """
    )


    # DELETED STUDENTS TABLE

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS deleted_students
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            deleted_date TEXT NOT NULL,
            deleted_time TEXT NOT NULL
        )
        """
    )


    # ADMIN TABLE

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS admin
        (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            admin_name TEXT NOT NULL
        )
        """
    )


    # CREATE DEFAULT ADMIN

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM admin
        """
    )


    admin_count = cursor.fetchone()[0]


    if admin_count == 0:

        cursor.execute(
            """
            INSERT INTO admin
            (
                id,
                username,
                password,
                admin_name
            )

            VALUES
            (
                1,
                ?,
                ?,
                ?
            )
            """,

            (
                "admin",
                "admin123",
                "Administrator"
            )
        )


    conn.commit()

    conn.close()


# ==================================================
# ADMIN STATUS
# ==================================================

admin_logged_in = False

current_admin_name = ""


# ==================================================
# START CAMERA
# ==================================================

def start_camera():

    main_file = os.path.join(
        BASE_DIR,
        "main.py"
    )


    if not os.path.exists(main_file):

        messagebox.showerror(
            "Error",
            "main.py file not found!"
        )

        return


    try:

        subprocess.Popen(
            [
                sys.executable,
                main_file
            ],

            cwd=BASE_DIR
        )


    except Exception as error:

        messagebox.showerror(
            "Camera Error",
            str(error)
        )


# ==================================================
# REGISTER STUDENT
# ==================================================

def register_student():

    register_file = os.path.join(
        BASE_DIR,
        "register.py"
    )


    if not os.path.exists(register_file):

        messagebox.showerror(
            "Error",
            "register.py file not found!"
        )

        return


    try:

        subprocess.Popen(
            [
                sys.executable,
                register_file
            ],

            cwd=BASE_DIR
        )


    except Exception as error:

        messagebox.showerror(
            "Registration Error",
            str(error)
        )


# ==================================================
# TRAIN AI MODEL
# ==================================================

def train_model():

    train_file = os.path.join(
        BASE_DIR,
        "train.py"
    )


    if not os.path.exists(train_file):

        messagebox.showerror(
            "Error",
            "train.py file not found!"
        )

        return


    try:

        subprocess.Popen(
            [
                sys.executable,
                train_file
            ],

            cwd=BASE_DIR
        )


    except Exception as error:

        messagebox.showerror(
            "Training Error",
            str(error)
        )


# ==================================================
# UPDATE STATISTICS
# ==================================================

def update_statistics():

    conn = connect_db()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM students
        """
    )


    total = cursor.fetchone()[0]


    registered_label.config(
        text=f"Total Students: {total}"
    )


    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    cursor.execute(
        """
        SELECT COUNT(DISTINCT student_id)
        FROM attendance
        WHERE date = ?
        """,

        (
            today,
        )
    )


    present = cursor.fetchone()[0]


    present_label.config(
        text=f"Present Today: {present}"
    )


    conn.close()


# ==================================================
# LOAD ATTENDANCE
# ==================================================

def load_attendance(data=None):

    for row in table.get_children():

        table.delete(
            row
        )


    conn = connect_db()

    cursor = conn.cursor()


    if data is None:

        cursor.execute(
            """
            SELECT
                date,
                time,
                student_id,
                student_name

            FROM attendance

            ORDER BY id DESC
            """
        )


        data = cursor.fetchall()


    conn.close()


    for row in data:

        table.insert(
            "",
            tk.END,
            values=row
        )


    update_statistics()


# ==================================================
# SEARCH ATTENDANCE
# ==================================================

def search_student():

    keyword = search_entry.get().strip()


    conn = connect_db()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            date,
            time,
            student_id,
            student_name

        FROM attendance

        WHERE
            student_name LIKE ?
            OR CAST(student_id AS TEXT) LIKE ?

        ORDER BY id DESC
        """,

        (
            "%" + keyword + "%",
            "%" + keyword + "%"
        )
    )


    result = cursor.fetchall()


    conn.close()


    load_attendance(
        result
    )


# ==================================================
# CLEAR SEARCH
# ==================================================

def clear_search():

    search_entry.delete(
        0,
        tk.END
    )


    load_attendance()


# ==================================================
# VIEW ALL STUDENTS
# ==================================================

def view_all_students():

    students_window = tk.Toplevel(
        window
    )


    students_window.title(
        "All Registered Students"
    )


    students_window.geometry(
        "650x450"
    )


    students_window.resizable(
        False,
        False
    )


    title = tk.Label(
        students_window,
        text="ALL REGISTERED STUDENTS",
        font=("Arial", 18, "bold")
    )


    title.pack(
        pady=15
    )


    columns = (
        "Student_ID",
        "Student_Name"
    )


    students_table = ttk.Treeview(
        students_window,
        columns=columns,
        show="headings"
    )


    students_table.heading(
        "Student_ID",
        text="Student ID"
    )


    students_table.heading(
        "Student_Name",
        text="Student Name"
    )


    students_table.column(
        "Student_ID",
        width=200,
        anchor="center"
    )


    students_table.column(
        "Student_Name",
        width=300,
        anchor="center"
    )


    students_table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )


    conn = connect_db()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            student_id,
            student_name

        FROM students

        ORDER BY student_id
        """
    )


    students = cursor.fetchall()


    conn.close()


    for student in students:

        students_table.insert(
            "",
            tk.END,
            values=student
        )


# ==================================================
# DELETE STUDENT
# ==================================================

def delete_student():

    delete_window = tk.Toplevel(
        window
    )


    delete_window.title(
        "Delete Student"
    )


    delete_window.geometry(
        "450x350"
    )


    delete_window.resizable(
        False,
        False
    )


    title = tk.Label(
        delete_window,
        text="DELETE STUDENT",
        font=("Arial", 18, "bold")
    )


    title.pack(
        pady=20
    )


    conn = connect_db()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            student_id,
            student_name

        FROM students

        ORDER BY student_id
        """
    )


    students = cursor.fetchall()


    conn.close()


    if len(students) == 0:

        messagebox.showinfo(
            "No Students",
            "No active students found.",
            parent=delete_window
        )


        delete_window.destroy()

        return


    student_values = [

        f"{student_id} - {student_name}"

        for student_id, student_name in students

    ]


    student_combo = ttk.Combobox(
        delete_window,
        values=student_values,
        width=35,
        state="readonly"
    )


    student_combo.pack(
        pady=15
    )


    student_combo.current(
        0
    )


    def confirm_delete():

        selected = student_combo.get()


        if selected == "":

            messagebox.showerror(
                "Error",
                "Please select a student.",
                parent=delete_window
            )

            return


        student_id_text = selected.split(
            " - ",
            1
        )[0]


        student_id = int(
            student_id_text
        )


        student_name = selected.split(
            " - ",
            1
        )[1]


        confirm = messagebox.askyesno(
            "Confirm Delete",

            f"Are you sure you want to delete:\n\n"
            f"ID: {student_id}\n"
            f"Name: {student_name}\n\n"
            f"Attendance history will be preserved.",

            parent=delete_window
        )


        if not confirm:

            return


        now = datetime.now()


        deleted_date = now.strftime(
            "%Y-%m-%d"
        )


        deleted_time = now.strftime(
            "%H:%M:%S"
        )


        conn = connect_db()

        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT INTO deleted_students
            (
                student_id,
                student_name,
                deleted_date,
                deleted_time
            )

            VALUES (?, ?, ?, ?)
            """,

            (
                student_id,
                student_name,
                deleted_date,
                deleted_time
            )
        )


        cursor.execute(
            """
            DELETE FROM students
            WHERE student_id = ?
            """,

            (
                student_id,
            )
        )


        conn.commit()

        conn.close()


        # UPDATE CSV

        if os.path.exists(CSV_FILE):

            remaining_students = []


            with open(
                CSV_FILE,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(
                    file
                )


                for row in reader:

                    try:

                        current_id = int(
                            row["Student_ID"]
                        )


                        if current_id != student_id:

                            remaining_students.append(
                                [
                                    current_id,
                                    row["Student_Name"]
                                ]
                            )


                    except:

                        continue


            with open(
                CSV_FILE,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file
                )


                writer.writerow(
                    [
                        "Student_ID",
                        "Student_Name"
                    ]
                )


                writer.writerows(
                    remaining_students
                )


        # DELETE FACE DATA

        deleted_images = 0


        if os.path.exists(DATASET_FOLDER):

            for filename in os.listdir(
                DATASET_FOLDER
            ):

                if filename.startswith(
                    f"User.{student_id}."
                ):

                    file_path = os.path.join(
                        DATASET_FOLDER,
                        filename
                    )


                    try:

                        os.remove(
                            file_path
                        )


                        deleted_images += 1


                    except Exception as error:

                        print(
                            "Could not delete:",
                            file_path,
                            error
                        )


        messagebox.showinfo(
            "Student Deleted",

            f"Student deleted successfully!\n\n"
            f"Student ID: {student_id}\n"
            f"Student Name: {student_name}\n\n"
            f"Face images deleted: {deleted_images}\n"
            f"Attendance history preserved."
        )


        delete_window.destroy()


        load_attendance()


    delete_button = tk.Button(
        delete_window,
        text="Delete Selected Student",
        width=28,
        height=2,
        command=confirm_delete
    )


    delete_button.pack(
        pady=20
    )


# ==================================================
# DELETED STUDENTS LIST
# ==================================================

def show_deleted_students():

    deleted_window = tk.Toplevel(
        window
    )


    deleted_window.title(
        "Deleted Students List"
    )


    deleted_window.geometry(
        "750x450"
    )


    columns = (
        "Student_ID",
        "Student_Name",
        "Deleted_Date",
        "Deleted_Time"
    )


    deleted_table = ttk.Treeview(
        deleted_window,
        columns=columns,
        show="headings"
    )


    for column in columns:

        deleted_table.heading(
            column,
            text=column
        )


        deleted_table.column(
            column,
            width=170
        )


    deleted_table.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )


    conn = connect_db()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            student_id,
            student_name,
            deleted_date,
            deleted_time

        FROM deleted_students

        ORDER BY id DESC
        """
    )


    deleted_students = cursor.fetchall()


    conn.close()


    for student in deleted_students:

        deleted_table.insert(
            "",
            tk.END,
            values=student
        )


# ==================================================
# EXPORT ATTENDANCE REPORT
# ==================================================

def export_report():

    conn = connect_db()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            date,
            time,
            student_id,
            student_name

        FROM attendance

        ORDER BY id DESC
        """
    )


    rows = cursor.fetchall()


    conn.close()


    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


    report_file = os.path.join(
        REPORT_FOLDER,
        f"Attendance_Report_{timestamp}.csv"
    )


    with open(
        report_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )


        writer.writerow(
            [
                "Date",
                "Time",
                "Student_ID",
                "Student_Name"
            ]
        )


        writer.writerows(
            rows
        )


    messagebox.showinfo(
        "Report Exported",

        f"Attendance report saved successfully!\n\n"
        f"Location:\n{report_file}"
    )


# ==================================================
# ADMIN LOGIN
# ==================================================

def admin_login():

    global admin_logged_in

    global current_admin_name


    login_window = tk.Toplevel(
        window
    )


    login_window.title(
        "Admin Login"
    )


    login_window.geometry(
        "450x350"
    )


    login_window.resizable(
        False,
        False
    )


    title = tk.Label(
        login_window,
        text="ADMIN LOGIN",
        font=("Arial", 20, "bold")
    )


    title.pack(
        pady=25
    )


    username_label = tk.Label(
        login_window,
        text="Username",
        font=("Arial", 12)
    )


    username_label.pack()


    username_entry = tk.Entry(
        login_window,
        width=30,
        font=("Arial", 12)
    )


    username_entry.pack(
        pady=8
    )


    password_label = tk.Label(
        login_window,
        text="Password",
        font=("Arial", 12)
    )


    password_label.pack()


    password_entry = tk.Entry(
        login_window,
        width=30,
        show="*",
        font=("Arial", 12)
    )


    password_entry.pack(
        pady=8
    )


    def verify_login():

        global admin_logged_in

        global current_admin_name


        username = username_entry.get().strip()

        password = password_entry.get().strip()


        conn = connect_db()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT
                admin_name

            FROM admin

            WHERE
                username = ?
                AND password = ?
            """,

            (
                username,
                password
            )
        )


        result = cursor.fetchone()


        conn.close()


        if result:

            admin_logged_in = True

            current_admin_name = result[0]


            login_window.destroy()


            update_admin_interface()


            messagebox.showinfo(
                "Admin Login",
                f"Welcome, {current_admin_name}!"
            )


        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password.",
                parent=login_window
            )


    login_button = tk.Button(
        login_window,
        text="LOGIN",
        width=25,
        height=2,
        command=verify_login
    )


    login_button.pack(
        pady=20
    )


    username_entry.focus()


    login_window.bind(
        "<Return>",
        lambda event: verify_login()
    )


# ==================================================
# CHANGE ADMIN
# ==================================================

def change_admin():

    if not admin_logged_in:

        return


    change_window = tk.Toplevel(
        window
    )


    change_window.title(
        "Change Admin Details"
    )


    change_window.geometry(
        "500x500"
    )


    change_window.resizable(
        False,
        False
    )


    title = tk.Label(
        change_window,
        text="CHANGE ADMIN DETAILS",
        font=("Arial", 18, "bold")
    )


    title.pack(
        pady=20
    )


    labels = [

        "Current Username",

        "Current Password",

        "New Username",

        "New Password",

        "Confirm New Password",

        "New Admin Name"

    ]


    entries = {}


    for label_text in labels:

        label = tk.Label(
            change_window,
            text=label_text,
            font=("Arial", 11)
        )


        label.pack()


        entry = tk.Entry(
            change_window,
            width=35,
            font=("Arial", 11)
        )


        if "Password" in label_text:

            entry.config(
                show="*"
            )


        entry.pack(
            pady=5
        )


        entries[label_text] = entry


    def save_admin_changes():

        current_username = entries[
            "Current Username"
        ].get().strip()


        current_password = entries[
            "Current Password"
        ].get().strip()


        new_username = entries[
            "New Username"
        ].get().strip()


        new_password = entries[
            "New Password"
        ].get().strip()


        confirm_password = entries[
            "Confirm New Password"
        ].get().strip()


        new_admin_name = entries[
            "New Admin Name"
        ].get().strip()


        if (

            current_username == ""

            or current_password == ""

            or new_username == ""

            or new_password == ""

            or confirm_password == ""

            or new_admin_name == ""

        ):

            messagebox.showerror(
                "Error",
                "All fields are required.",
                parent=change_window
            )

            return


        if new_password != confirm_password:

            messagebox.showerror(
                "Password Error",
                "New passwords do not match.",
                parent=change_window
            )

            return


        conn = connect_db()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT
                id

            FROM admin

            WHERE
                username = ?

                AND password = ?
            """,

            (
                current_username,
                current_password
            )
        )


        valid_admin = cursor.fetchone()


        if valid_admin is None:

            conn.close()


            messagebox.showerror(
                "Verification Failed",
                "Current admin username or password is incorrect.",
                parent=change_window
            )

            return


        cursor.execute(
            """
            UPDATE admin

            SET
                username = ?,
                password = ?,
                admin_name = ?

            WHERE id = 1
            """,

            (
                new_username,
                new_password,
                new_admin_name
            )
        )


        conn.commit()

        conn.close()


        global current_admin_name


        current_admin_name = new_admin_name


        admin_name_label.config(
            text=f"Admin: {current_admin_name}"
        )


        messagebox.showinfo(
            "Success",
            "Admin details updated successfully.",
            parent=change_window
        )


        change_window.destroy()


    save_button = tk.Button(
        change_window,
        text="SAVE CHANGES",
        width=25,
        height=2,
        command=save_admin_changes
    )


    save_button.pack(
        pady=20
    )


# ==================================================
# ADMIN LOGOUT
# ==================================================

def admin_logout():

    global admin_logged_in

    global current_admin_name


    admin_logged_in = False

    current_admin_name = ""


    update_admin_interface()


    messagebox.showinfo(
        "Logout",
        "Admin logged out successfully."
    )


# ==================================================
# UPDATE ADMIN INTERFACE
# ==================================================

def update_admin_interface():

    if admin_logged_in:

        # HIDE NORMAL USER FRAME

        basic_frame.pack_forget()


        # SHOW ADMIN BUTTONS

        admin_button_frame.pack(
            pady=10
        )


        admin_control_frame.pack(
            pady=5
        )


        # UPDATE ADMIN NAME

        admin_name_label.config(
            text=f"Admin: {current_admin_name}"
        )


        admin_login_button.config(
            text="Admin Panel Active",
            state=tk.DISABLED
        )


        change_admin_button.config(
            state=tk.NORMAL
        )


        logout_button.config(
            state=tk.NORMAL
        )


    else:

        # HIDE ADMIN BUTTONS

        admin_button_frame.pack_forget()


        admin_control_frame.pack_forget()


        # SHOW NORMAL USER FRAME

        basic_frame.pack(
            pady=15
        )


        # UPDATE ADMIN NAME

        admin_name_label.config(
            text="Admin: Not Logged In"
        )


        admin_login_button.config(
            text="Admin Login",
            state=tk.NORMAL
        )


        change_admin_button.config(
            state=tk.DISABLED
        )


        logout_button.config(
            state=tk.DISABLED
        )


# ==================================================
# INITIALIZE DATABASE
# ==================================================

initialize_database()


# ==================================================
# MAIN WINDOW
# ==================================================

window = tk.Tk()


window.title(
    "AI Smart Attendance System"
)


window.geometry(
    "1100x850"
)


window.configure(
    bg="#1e1e2f"
)


# ==================================================
# HEADER
# ==================================================

header = tk.Frame(
    window,
    bg="#252545",
    height=110
)


header.pack(
    fill="x"
)


title = tk.Label(
    header,
    text="AI SMART ATTENDANCE SYSTEM",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#252545"
)


title.pack(
    pady=10
)


subtitle = tk.Label(
    header,
    text="Face Recognition Based Attendance Management",
    font=("Arial", 12),
    fg="white",
    bg="#252545"
)


subtitle.pack()


admin_name_label = tk.Label(
    header,
    text="Admin: Not Logged In",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#252545"
)


admin_name_label.pack(
    pady=5
)


# ==================================================
# STATISTICS
# ==================================================

stats_frame = tk.Frame(
    window,
    bg="#1e1e2f"
)


stats_frame.pack(
    pady=15
)


registered_label = tk.Label(
    stats_frame,
    text="Total Students: 0",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#1e1e2f"
)


registered_label.grid(
    row=0,
    column=0,
    padx=40
)


present_label = tk.Label(
    stats_frame,
    text="Present Today: 0",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#1e1e2f"
)


present_label.grid(
    row=0,
    column=1,
    padx=40
)


# ==================================================
# CONTENT FRAME
# ==================================================

content_frame = tk.Frame(
    window,
    bg="#1e1e2f"
)


content_frame.pack(
    fill="both",
    expand=True
)


# ==================================================
# NORMAL USER FRAME
# ==================================================

basic_frame = tk.Frame(
    content_frame,
    bg="#1e1e2f"
)


basic_frame.pack(
    pady=15
)


start_camera_button = tk.Button(
    basic_frame,
    text="Start Camera",
    width=22,
    height=2,
    command=start_camera
)


start_camera_button.grid(
    row=0,
    column=0,
    padx=10
)


admin_login_button = tk.Button(
    basic_frame,
    text="Admin Login",
    width=22,
    height=2,
    command=admin_login
)


admin_login_button.grid(
    row=0,
    column=1,
    padx=10
)


# ==================================================
# ADMIN BUTTON FRAME
# ==================================================

admin_button_frame = tk.Frame(
    content_frame,
    bg="#1e1e2f"
)


admin_button_data = [

    (
        "Register Student",
        register_student
    ),

    (
        "Train AI Model",
        train_model
    ),

    (
        "Delete Student",
        delete_student
    ),

    (
        "Deleted Students List",
        show_deleted_students
    ),

    (
        "View All Students",
        view_all_students
    ),

    (
        "Export Report",
        export_report
    )

]


for i, (text, command) in enumerate(
    admin_button_data
):

    tk.Button(
        admin_button_frame,
        text=text,
        width=22,
        height=2,
        command=command
    ).grid(
        row=i // 3,
        column=i % 3,
        padx=10,
        pady=8
    )


# ==================================================
# ADMIN CONTROL FRAME
# ==================================================

admin_control_frame = tk.Frame(
    content_frame,
    bg="#1e1e2f"
)


change_admin_button = tk.Button(
    admin_control_frame,
    text="Change Admin",
    width=22,
    height=2,
    command=change_admin,
    state=tk.DISABLED
)


change_admin_button.grid(
    row=0,
    column=0,
    padx=10
)


logout_button = tk.Button(
    admin_control_frame,
    text="Admin Logout",
    width=22,
    height=2,
    command=admin_logout,
    state=tk.DISABLED
)


logout_button.grid(
    row=0,
    column=1,
    padx=10
)


# ==================================================
# SEARCH FRAME
# ==================================================

search_frame = tk.Frame(
    content_frame,
    bg="#1e1e2f"
)


search_frame.pack(
    pady=10
)


search_entry = tk.Entry(
    search_frame,
    width=30
)


search_entry.grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(
    search_frame,
    text="Search",
    command=search_student
).grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(
    search_frame,
    text="Clear",
    command=clear_search
).grid(
    row=0,
    column=2,
    padx=5
)


# ==================================================
# ATTENDANCE TABLE
# ==================================================

columns = (

    "Date",

    "Time",

    "Student_ID",

    "Student_Name"

)


table = ttk.Treeview(
    content_frame,
    columns=columns,
    show="headings",
    height=12
)


for col in columns:

    table.heading(
        col,
        text=col
    )


    table.column(
        col,
        width=220
    )


table.pack(
    pady=20
)


# ==================================================
# EXIT BUTTON
# ==================================================

tk.Button(
    content_frame,
    text="Exit",
    width=20,
    command=window.destroy
).pack(
    pady=5
)


# ==================================================
# INITIAL LOAD
# ==================================================

load_attendance()


# ==================================================
# INITIAL ADMIN INTERFACE
# ==================================================

update_admin_interface()


# ==================================================
# START DASHBOARD
# ==================================================

window.mainloop()