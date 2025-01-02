import tkinter as tk
from tkinter import ttk, messagebox
from project import Project
from task import Task
from team_member import TeamMember
from utils import load_from_json, save_to_json

DATA_FILE = "example.json"

# Initiate global project list
projects = []

def main_window(projects, save_projects):
    root.tk.Tk()
    root.title("Project Management App")
    root.geometry("800x600")

    tk.Label(root, text='Project Management App', font=("Arial", 24)).pack(pady=20)

    def view_projects():
        view_projects_window = tk.TopLevel(root)
        view_projects_window.title("All Projects")
        columns = ("Name", "Description", "Deadline")
        tree = ttk.Treeview(view_projecrs_window, columns=columns, show = "headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        for project in projects:
            tree.insert("", tk.END, values=(project.name, project.desc, project .deadline))
        tree.pack(fill=tk.BOTH, expand=True)
    
    def create_project():
        def dsave_new_project():
            name = name_entry.get()
            desc = desc_entry.get()
            if not name or not deadline:
                messagebox.showerror("Error", "Name and deadline are required.")
                return
            projects.append(Project(name, desc, deadline))
            messagebox.showinfo("Success", f"Projecr {name} created!")
            create_project_window.destroy()

        create_project_window = tk.Toplevel(root)
        create_project_window.title("New Project")
        tk.Label(create_project_window, text = "Name:").pack(pady=5)



    def on_exit():
        save_projects()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_exit)
    root.mainloop()
