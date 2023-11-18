import tkinter as tk
from tkinter import ttk
import os
import subprocess

def run_options():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "options.pyw")
    subprocess.Popen(["pythonw", script_path], creationflags=subprocess.CREATE_NO_WINDOW)

def run_taskilla():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "taskilla.pyw")
    subprocess.Popen(["pythonw", script_path], creationflags=subprocess.CREATE_NO_WINDOW)

def create_main_window():
    root = tk.Tk()
    root.title("taskilla menu")
    script_dir = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(script_dir, "icon.png")
    root.iconphoto(True, tk.PhotoImage(file=icon_path))
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    options_button = ttk.Button(main_frame, text="Run Options", command=run_options)
    options_button.grid(column=0, row=0, padx=20, pady=20)
    taskilla_button = ttk.Button(main_frame, text="Run Taskilla", command=run_taskilla)
    taskilla_button.grid(column=1, row=0, padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()