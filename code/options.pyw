import tkinter as tk
from tkinter import Checkbutton, IntVar, Canvas, Frame, Scrollbar
import os
import psutil

def get_all_services():
    return [service.name() for service in psutil.win_service_iter()]

def save_selected_services(selected_services):
    with open("selected_services.txt", "w") as file:
        for service in selected_services:
            file.write(service + "\n")

class ScrollableServiceList(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.scrollbar.pack(side="right", fill="y")

        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.frame_id, width=event.width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def populate(self, services, service_vars):
        for idx, service in enumerate(services):
            checkbox = Checkbutton(self.frame, text=service, variable=service_vars[idx])
            checkbox.pack(anchor="w")

        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

def on_select(evt):
    selected_services = [listbox.get(idx) for idx in listbox.curselection()]
    for var, service in zip(service_vars, all_services):
        var.set(1 if service in selected_services else 0)

def select_services():
    root = tk.Tk()
    root.title("select services")
    script_dir = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(script_dir, "icon.png")
    root.iconphoto(True, tk.PhotoImage(file=icon_path))

    all_services = get_all_services()
    service_vars = [IntVar() for _ in all_services]

    scrollable_frame = ScrollableServiceList(root)
    scrollable_frame.pack(fill="both", expand=True)

    scrollable_frame.populate(all_services, service_vars)

    listbox = scrollable_frame.frame
    listbox.bind("<<Configure>>", on_select)

    def save_and_close():
        selected_services = [service for service, selected in zip(all_services, service_vars) if selected.get()]
        save_selected_services(selected_services)
        root.destroy()

    button = tk.Button(root, text="Save and Close", command=save_and_close)
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    select_services()
