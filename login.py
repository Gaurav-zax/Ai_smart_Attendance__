import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os


# ==================================================
# PROJECT PATH
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==================================================
# LOGIN DETAILS
# ==================================================

USERNAME = "admin"
PASSWORD = "admin123"


# ==================================================
# OPEN DASHBOARD
# ==================================================

def open_dashboard():

    username = username_entry.get().strip()

    password = password_entry.get().strip()


    if username == USERNAME and password == PASSWORD:

        login_window.destroy()


        dashboard_file = os.path.join(

            BASE_DIR,

            "database.py"

        )


        subprocess.Popen(

            [

                sys.executable,

                dashboard_file

            ],

            cwd=BASE_DIR

        )


    else:

        messagebox.showerror(

            "Login Failed",

            "Invalid Username or Password!"

        )


# ==================================================
# LOGIN WINDOW
# ==================================================

login_window = tk.Tk()


login_window.title(

    "AI Smart Attendance - Login"

)


login_window.geometry(

    "450x350"

)


login_window.resizable(

    False,

    False

)


# ==================================================
# TITLE
# ==================================================

title_label = tk.Label(

    login_window,

    text="AI SMART ATTENDANCE SYSTEM",

    font=(

        "Arial",

        18,

        "bold"

    )

)


title_label.pack(

    pady=30

)


# ==================================================
# USERNAME
# ==================================================

username_label = tk.Label(

    login_window,

    text="Username",

    font=(

        "Arial",

        12

    )

)


username_label.pack()


username_entry = tk.Entry(

    login_window,

    width=30,

    font=(

        "Arial",

        12

    )

)


username_entry.pack(

    pady=8

)


# ==================================================
# PASSWORD
# ==================================================

password_label = tk.Label(

    login_window,

    text="Password",

    font=(

        "Arial",

        12

    )

)


password_label.pack()


password_entry = tk.Entry(

    login_window,

    width=30,

    show="*",

    font=(

        "Arial",

        12

    )

)


password_entry.pack(

    pady=8

)


# ==================================================
# LOGIN BUTTON
# ==================================================

login_button = tk.Button(

    login_window,

    text="LOGIN",

    width=25,

    height=2,

    command=open_dashboard

)


login_button.pack(

    pady=20

)


# ==================================================
# ENTER KEY LOGIN
# ==================================================

login_window.bind(

    "<Return>",

    lambda event: open_dashboard()

)


username_entry.focus()


# ==================================================
# START LOGIN
# ==================================================

login_window.mainloop()