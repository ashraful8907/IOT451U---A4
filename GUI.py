import tkinter as tk
from tkinter import ttk, messagebox
from project import Project
from task import Task
from team_member import TeamMember
from utils import load_from_json, save_to_json
import datetime

DATA_FILE = "example.json"

# Initiate global project list
projects = []

def save_projects():
    save_to_json(DATA_FILE, [proj.to_dict() for proj in projects])

def main_window(projects, save_projects):
    root = tk.Tk()
    root.title("Project Management App")
    root.geometry("800x600")

    tk.Label(root, text='Project Management App', font=("Arial", 24)).pack(pady=20)

    def is_valid_date(date_str):
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def view_projects():
        view_projects_window = tk.Toplevel(root)
        view_projects_window.title("All Projects")
        columns = ("Name", "Description", "Deadline")
        tree = ttk.Treeview(view_projects_window, columns=columns, show = "headings")
        for col in columns:
            tree.heading(col, text=col)
            if col == "Description":
                tree.column(col, width=300)
            else:
                tree.column(col, width=150)
        for project in projects:
            tree.insert("", tk.END, values=(project.name, project.desc, project .deadline))
        tree.pack(fill=tk.BOTH, expand=True)
    
    def create_project():
        def save_new_project():
            name = name_entry.get()
            desc = desc_entry.get()
            deadline = deadline_entry.get()
            if not name or not deadline:
                messagebox.showerror("Error", "Name and deadline are required.")
                return
            if not is_valid_date(deadline):
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return
            projects.append(Project(name, desc, deadline))
            messagebox.showinfo("Success", f"Project {name} created!")
            create_project_window.destroy()

        create_project_window = tk.Toplevel(root)
        create_project_window.title("New Project")
        tk.Label(create_project_window, text = "Name:").pack(pady=5)
        name_entry = tk.Entry(create_project_window)
        name_entry.pack()
        tk.Label(create_project_window, text="Description:").pack(pady=5)
        desc_entry = tk.Entry(create_project_window)
        desc_entry.pack()
        tk.Label(create_project_window, text="Deadline (YYYY-MM-DD):").pack(pady=5)
        deadline_entry = tk.Entry(create_project_window)
        deadline_entry.pack()
        tk.Button(create_project_window, text="Save", command=save_new_project).pack(pady=5)

    tk.Button(root, text="View Projects", command=view_projects).pack(pady=10)
    tk.Button(root, text="Create Project", command=create_project).pack(pady=10)

    def on_exit():
        save_projects()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_exit)
    root.mainloop()
