import subprocess
import sys
import ctypes
import os
import tkinter as tk
from tkinter import messagebox
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def stop_selected_services():
    result_text = ""
    try:
        with open("selected_services.txt", "r") as file:
            selected_services = [line.strip() for line in file.readlines()]

        if not selected_services:
            messagebox.showinfo("no services selected", "select services in options before running taskilla.")
            sys.exit()
        for service in selected_services:
            try:
                subprocess.run(['sc', 'stop', service], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                result_text += f"{service} killed\n"
            except subprocess.CalledProcessError as e:
                if "1062" in str(e):
                    result_text += f"{service} not running\n"
                else:
                    result_text += f"error to kill {service}\n"
    except FileNotFoundError:
        result_text = "no services have been selected to kill"

    return result_text

def show_result_message():
    result = stop_selected_services()
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("taskilla", result)

# Stop services and show result
show_result_message()
