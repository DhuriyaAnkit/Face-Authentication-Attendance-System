import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")

PYTHON = sys.executable


def run_script(script_name):
    script_path = os.path.join(SRC_DIR, script_name)
    try:
        subprocess.run([PYTHON, script_path])
        status_label.config(text=f"{script_name} finished")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def register_user():
    status_label.config(text="Registering user...")
    run_script("register_user.py")


def start_attendance():
    status_label.config(text="Attendance running...")
    run_script("attendance.py")


def delete_user():
    status_label.config(text="Deleting user...")
    run_script("delete_user.py")


# ---------------- UI ----------------
root = tk.Tk()
root.title("Face Authentication Attendance System")
root.geometry("420x350")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Face Authentication System",
    font=("Arial", 18, "bold")
)
title.pack(pady=20)

btn_register = tk.Button(
    root,
    text="Register New User",
    width=25,
    height=2,
    font=("Arial", 12),
    command=register_user
)
btn_register.pack(pady=10)

btn_attendance = tk.Button(
    root,
    text="Start Attendance",
    width=25,
    height=2,
    font=("Arial", 12),
    command=start_attendance
)
btn_attendance.pack(pady=10)

btn_delete = tk.Button(
    root,
    text="Delete User",
    width=25,
    height=2,
    font=("Arial", 12),
    command=delete_user
)
btn_delete.pack(pady=10)

status_label = tk.Label(
    root,
    text="Status: Ready",
    font=("Arial", 10),
    fg="green"
)
status_label.pack(pady=20)

root.mainloop()
