import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import csv
import os
import shutil
from datetime import datetime



# Main Window

window = tk.Tk()

window.title("AI Smart Attendance System")

window.geometry("1000x750")

window.configure(
    bg="#1e1e2f"
)



# ---------- Header ----------


header = tk.Frame(
    window,
    bg="#252545",
    height=100
)

header.pack(
    fill="x"
)



title = tk.Label(
    header,
    text="AI SMART ATTENDANCE SYSTEM",
    font=("Arial",24,"bold"),
    fg="white",
    bg="#252545"
)

title.pack(
    pady=10
)



subtitle = tk.Label(
    header,
    text="Face Recognition Based Attendance Management",
    font=("Arial",12),
    fg="#dddddd",
    bg="#252545"
)

subtitle.pack()



# ---------- Statistics ----------


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
    font=("Arial",14,"bold"),
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
    font=("Arial",14,"bold"),
    fg="white",
    bg="#1e1e2f"
)

present_label.grid(
    row=0,
    column=1,
    padx=40
)



# ---------- Functions ----------


def start_camera():

    subprocess.Popen(
        ["python","main.py"]
    )



def register_student():

    subprocess.Popen(
        ["python","register.py"]
    )



def train_model():

    subprocess.Popen(
        ["python","train.py"]
    )



def update_statistics():

    count = 0


    if os.path.exists("students.csv"):

        with open("students.csv","r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                count += 1


    registered_label.config(
        text=f"Total Students: {count}"
    )



    present=set()


    if os.path.exists("attendance.csv"):

        today=datetime.now().strftime("%Y-%m-%d")


        with open("attendance.csv","r") as file:

            reader=csv.DictReader(file)


            for row in reader:

                if row["Date"] == today:

                    present.add(
                        row["Student_ID"]
                    )



    present_label.config(
        text=f"Present Today: {len(present)}"
    )


# ---------- Attendance Load ----------


def load_attendance(data=None):

    for row in table.get_children():

        table.delete(row)



    if data is None:

        data=[]


        if os.path.exists("attendance.csv"):


            with open("attendance.csv","r") as file:


                reader=csv.DictReader(file)


                for row in reader:

                    data.append(row)




    for row in data:


        table.insert(
            "",
            tk.END,
            values=(
                row["Date"],
                row["Time"],
                row["Student_ID"],
                row["Student_Name"]
            )
        )



    update_statistics()




# Search Student

def search_student():


    keyword = search_entry.get().lower()


    results=[]


    if os.path.exists("attendance.csv"):


        with open("attendance.csv","r") as file:


            reader=csv.DictReader(file)


            for row in reader:


                if (
                    keyword in row["Student_Name"].lower()
                    or keyword in row["Student_ID"]
                ):

                    results.append(row)



    load_attendance(results)




def clear_search():

    search_entry.delete(
        0,
        tk.END
    )

    load_attendance()





# Export Report

def export_report():


    if os.path.exists("attendance.csv"):


        shutil.copy(
            "attendance.csv",
            "Attendance_Report.csv"
        )


        messagebox.showinfo(
            "Success",
            "Attendance Report Generated Successfully!"
        )


    else:

        messagebox.showwarning(
            "Warning",
            "Attendance file not found"
        )





# ---------- Buttons ----------


button_frame=tk.Frame(
    window,
    bg="#1e1e2f"
)

button_frame.pack(
    pady=15
)



buttons=[
    ("Start Camera",start_camera,"#28a745"),
    ("Register Student",register_student,"#007bff"),
    ("Train AI Model",train_model,"#ff9800"),
    ("Refresh Attendance",load_attendance,"#9c27b0"),
    ("Export Report",export_report,"#e91e63")
]



for i,(text,command,color) in enumerate(buttons):

    tk.Button(
        button_frame,
        text=text,
        width=22,
        height=2,
        bg=color,
        fg="white",
        font=("Arial",11,"bold"),
        command=command
    ).grid(
        row=i//3,
        column=i%3,
        padx=10,
        pady=8
    )





# ---------- Search ----------


search_frame=tk.Frame(
    window,
    bg="#1e1e2f"
)

search_frame.pack(
    pady=10
)



tk.Label(
    search_frame,
    text="Search Student:",
    fg="white",
    bg="#1e1e2f",
    font=("Arial",12)
).grid(
    row=0,
    column=0
)



search_entry=tk.Entry(
    search_frame,
    width=25,
    font=("Arial",12)
)

search_entry.grid(
    row=0,
    column=1,
    padx=10
)



tk.Button(
    search_frame,
    text="Search",
    command=search_student
).grid(
    row=0,
    column=2,
    padx=5
)



tk.Button(
    search_frame,
    text="Clear",
    command=clear_search
).grid(
    row=0,
    column=3,
    padx=5
)





# ---------- Attendance Table ----------


columns=(
    "Date",
    "Time",
    "Student_ID",
    "Student_Name"
)



style=ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="#2b2b3d",
    foreground="white",
    rowheight=30,
    fieldbackground="#2b2b3d"
)



table=ttk.Treeview(
    window,
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
        width=200
    )



table.pack(
    pady=20
)





# Status Bar


status = tk.Label(
    window,
    text="System Status: READY | AI Model Loaded",
    fg="#00ff00",
    bg="#1e1e2f",
    font=("Arial",12)
)

status.pack(
    pady=10
)





# Exit

tk.Button(
    window,
    text="Exit",
    width=20,
    height=2,
    bg="red",
    fg="white",
    command=window.destroy
).pack()



# Initial Load

update_statistics()

load_attendance()



window.mainloop()