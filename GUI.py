import customtkinter as ctk
from tkinter import messagebox, Toplevel
from classes import Project, Task, TeamMember
from datetime import datetime

# Main GUI Function
def main_window(projects, save_projects):
    # Initialize Application
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Project Management App")
    root.geometry("1000x700")

    # Helper Functions
    def update_stats():
        """Update the statistics display."""
        total_projects = len(projects)
        total_tasks = sum(len(proj.tasks) for proj in projects)
        completed_tasks = sum(
            1 for proj in projects for task in proj.tasks if task.status == "Completed"
        )
        stats_label.configure(
            text=f"Total Projects: {total_projects} | Total Tasks: {total_tasks} | Completed Tasks: {completed_tasks}"
        )

    def create_project():
        """Open a window to create a new project."""
        def save_new_project():
            name = project_name_entry.get()
            description = project_desc_entry.get()
            deadline = project_deadline_entry.get()
            if not name or not deadline:
                messagebox.showerror("Error", "Project name and deadline are required.")
                return
            try:
                new_project = Project(name=name, description=description, deadline=deadline)
                projects.append(new_project)
                update_stats()
                create_window.destroy()
                messagebox.showinfo("Success", f"Project '{name}' created successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        create_window = Toplevel(root)
        create_window.title("Create New Project")
        create_window.geometry("400x300")

        ctk.CTkLabel(create_window, text="Project Name:", text_color= "black").pack(pady=5)
        project_name_entry = ctk.CTkEntry(create_window, width=300)
        project_name_entry.pack()

        ctk.CTkLabel(create_window, text="Description:", text_color= "black").pack(pady=5)
        project_desc_entry = ctk.CTkEntry(create_window, width=300)
        project_desc_entry.pack()

        ctk.CTkLabel(create_window, text="Deadline (YYYY-MM-DD):", text_color= "black").pack(pady=5)
        project_deadline_entry = ctk.CTkEntry(create_window, width=300)
        project_deadline_entry.pack()

        ctk.CTkButton(
            create_window, text="Save", command=save_new_project, fg_color="#007AFF"
        ).pack(pady=10)

    def add_task():
        """Add a new task to a selected project."""
        def save_new_task():
            project_name = project_dropdown.get()
            task_name = task_name_entry.get()
            description = task_desc_entry.get()
            due_date = task_due_date_entry.get()
            priority = task_priority_dropdown.get()

            if not project_name or not task_name or not due_date:
                messagebox.showerror("Error", "Project, task name, and due date are required.")
                return

            selected_project = next((proj for proj in projects if proj.name == project_name), None)
            if not selected_project:
                messagebox.showerror("Error", f"Project '{project_name}' not found.")
                return

            try:
                new_task = Task(
                    name=task_name,
                    description=description,
                    due_date=due_date,
                    priority=priority,
                )
                selected_project.add_task(new_task)
                update_stats()
                add_task_window.destroy()
                messagebox.showinfo("Success", f"Task '{task_name}' added to project '{project_name}'.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        add_task_window = Toplevel(root)
        add_task_window.title("Add Task")
        add_task_window.geometry("400x400")

        ctk.CTkLabel(add_task_window, text="Select Project:", text_color= "black").pack(pady=5)
        project_dropdown = ctk.CTkComboBox(add_task_window, values=[proj.name for proj in projects])
        project_dropdown.pack()

        ctk.CTkLabel(add_task_window, text="Task Name:", text_color= "black").pack(pady=5)
        task_name_entry = ctk.CTkEntry(add_task_window, width=300)
        task_name_entry.pack()

        ctk.CTkLabel(add_task_window, text="Description:", text_color= "black").pack(pady=5)
        task_desc_entry = ctk.CTkEntry(add_task_window, width=300)
        task_desc_entry.pack()

        ctk.CTkLabel(add_task_window, text="Due Date (YYYY-MM-DD):", text_color= "black").pack(pady=5)
        task_due_date_entry = ctk.CTkEntry(add_task_window, width=300)
        task_due_date_entry.pack()

        ctk.CTkLabel(add_task_window, text="Priority:", text_color= "black").pack(pady=5)
        task_priority_dropdown = ctk.CTkComboBox(add_task_window, values=["Low", "Medium", "High"])
        task_priority_dropdown.pack()

        ctk.CTkButton(
            add_task_window, text="Save Task", command=save_new_task, fg_color="#007AFF"
        ).pack(pady=10)

    def assign_task():
        """Assign a task to a team member."""
        def save_assignee():
            assignee_name = assignee_entry.get()
            project_name = project_dropdown.get()
            task_title = task_dropdown.get()

            if not project_name or not task_title:
                messagebox.showerror("Error", "Please select a project and a task.")
                return

            selected_project = next((proj for proj in projects if proj.name == project_name), None)
            if not selected_project:
                messagebox.showerror("Error", f"Project '{project_name}' not found.")
                return

            selected_task = next((task for task in selected_project.tasks if task.name == task_title), None)
            if not selected_task:
                messagebox.showerror("Error", f"Task '{task_title}' not found.")
                return

            selected_task.assignee = TeamMember(name=assignee_name, description="", role="Assigned")
            messagebox.showinfo("Success", f"Task '{selected_task.name}' assigned to {assignee_name}.")
            assign_window.destroy()  # Close the window after assigning

        def update_tasks(event):
            project_name = project_dropdown.get()
            selected_project = next((proj for proj in projects if proj.name == project_name), None)
            if selected_project:
                task_dropdown.configure(values=[task.name for task in selected_project.tasks])
                task_dropdown.set("")  # Reset task dropdown when a project is selected
            else:
                task_dropdown.configure(values=[])

        # Assign Task Window
        assign_window = Toplevel(root)
        assign_window.title("Assign Task")
        assign_window.resizable(False, False)
        assign_window.geometry("800x800")

        # Select Project Dropdown
        ctk.CTkLabel(assign_window, text="Select Project:", text_color="black").pack(pady=10)
        project_dropdown = ctk.CTkComboBox(assign_window, values=[proj.name for proj in projects])
        project_dropdown.pack(pady=5)
        project_dropdown.bind("<<ComboboxSelected>>", update_tasks)

        # Select Task Dropdown
        ctk.CTkLabel(assign_window, text="Select Task:", text_color="black").pack(pady=10)
        task_dropdown = ctk.CTkComboBox(assign_window, values=[])
        task_dropdown.pack(pady=5)

        # Enter Assignee Name
        ctk.CTkLabel(assign_window, text="Assignee Name:", text_color="black").pack(pady=10)
        assignee_entry = ctk.CTkEntry(assign_window, width=300)
        assignee_entry.pack(pady=5)

        # Assign Button
        assign_button = ctk.CTkButton(assign_window, text="Assign", command=save_assignee, fg_color="#007AFF")
        assign_button.pack(pady=20)  # Add spacing around the button

    def view_tasks():
        """Display tasks grouped by project."""
        view_tasks_window = Toplevel(root)
        view_tasks_window.title("View Tasks")
        view_tasks_window.geometry("600x400")

        for proj in projects:
            ctk.CTkLabel(view_tasks_window, text=f"Project: {proj.name}", font=("Helvetica Neue", 16), text_color= "black").pack(pady=5)
            for task in proj.tasks:
                task_info = (f"  - {task.name} | Status: {task.status} | "
                             f"Due: {task.due_date.strftime('%Y-%m-%d')} | Priority: {task.priority}")
                ctk.CTkLabel(view_tasks_window, text=task_info, text_color= "black").pack()

    def view_workload():
        """Display workload for all team members."""
        workload_window = Toplevel(root)
        workload_window.title("Team Member Workload")
        workload_window.geometry("600x400")

        member_workload = {}
        for proj in projects:
            for task in proj.tasks:
                if task.assignee:
                    member_workload.setdefault(task.assignee.name, []).append(task.name)

        for member, tasks in member_workload.items():
            ctk.CTkLabel(workload_window, text=f"{member}:", font=("Helvetica Neue", 16), text_color= "black").pack(pady=5)
            for task in tasks:
                ctk.CTkLabel(workload_window, text=f"  - {task}", text_color= "black").pack()

    def filter_tasks():
        """Filter tasks based on their status."""
        def apply_filter():
            selected_status = status_dropdown.get()
            filtered_tasks = [
                f"{task.name} (Project: {proj.name})"
                for proj in projects
                for task in proj.tasks
                if task.status == selected_status
            ]
            results_label.configure(
                text="\n".join(filtered_tasks) if filtered_tasks else "No tasks found."
            )

        filter_window = Toplevel(root)
        filter_window.title("Filter Tasks")
        filter_window.geometry("400x300")

        ctk.CTkLabel(filter_window, text="Select Status to Filter:", text_color= "black").pack(pady=10)
        status_dropdown = ctk.CTkComboBox(filter_window, values=["Not Started", "In Progress", "Completed"])
        status_dropdown.pack()

        ctk.CTkButton(filter_window, text="Apply Filter", command=apply_filter, fg_color="#007AFF").pack(pady=10)

        results_label = ctk.CTkLabel(filter_window, text="", text_color= "black")
        results_label.pack(pady=10)

    def check_overdue():
        """Check for overdue tasks."""
        overdue_tasks = []
        today = datetime.today()

        for proj in projects:
            for task in proj.tasks:
                if task.due_date < today and task.status != "Completed":
                    overdue_tasks.append(f"{task.name} (Project: {proj.name})")

        if overdue_tasks:
            messagebox.showinfo("Overdue Tasks", "\n".join(overdue_tasks))
        else:
            messagebox.showinfo("Overdue Tasks", "No overdue tasks!")

    def view_projects():
        """Display a list of all projects and their details."""
        view_window = Toplevel(root)
        view_window.title("View Projects")
        view_window.geometry("600x400")

        if not projects:
            ctk.CTkLabel(view_window, text="No projects available.", font=("Helvetica Neue", 16), text_color= "black").pack(pady=20)
            return

        for proj in projects:
            project_label = ctk.CTkLabel(
                view_window,
                text=f"Project: {proj.name}\nDescription: {proj.description}\nDeadline: {proj.deadline.strftime('%Y-%m-%d')}",
                font=("Helvetica Neue", 14),
                justify="left",
                anchor="w",
                wraplength=500,
            )
            project_label.pack(pady=10, anchor="w")

            if proj.tasks:
                task_label = ctk.CTkLabel(view_window, text="Tasks:", font=("Helvetica Neue", 12, "bold"), text_color= "black")
                task_label.pack(anchor="w")
                for task in proj.tasks:
                    task_info = f"  - {task.name} | Status: {task.status} | Priority: {task.priority} | Due: {task.due_date.strftime('%Y-%m-%d')}"
                    task_item = ctk.CTkLabel(view_window, text=task_info, font=("Helvetica Neue", 12), justify="left", anchor="w", text_color= "black")
                    task_item.pack(anchor="w")
            else:
                no_tasks_label = ctk.CTkLabel(view_window, text="  No tasks added yet.", font=("Helvetica Neue", 12), text_color= "black")
                no_tasks_label.pack(anchor="w")

    # Header Section
    header_frame = ctk.CTkFrame(root, height=80, corner_radius=15)
    header_frame.pack(fill="x", pady=10)
    header_label = ctk.CTkLabel(
        header_frame,
        text="Project Management App",
        font=("Helvetica Neue", 28, "bold"),
    )
    header_label.pack(pady=20)

    # Stats Section
    stats_frame = ctk.CTkFrame(root, corner_radius=15)
    stats_frame.pack(pady=20, padx=20, fill="x")
    stats_label = ctk.CTkLabel(
        stats_frame,
        text="Total Projects: 0 | Total Tasks: 0 | Completed Tasks: 0",
        font=("Helvetica Neue", 18),
    )
    stats_label.pack(pady=10)

    # Action Buttons
    button_frame = ctk.CTkFrame(root, corner_radius=15)
    button_frame.pack(pady=20, padx=20, expand=True)

    actions = [
        ("Create Project", create_project),
        ("View Projects", view_projects),
        ("Add Task to Project", add_task),
        ("Assign Task to Team Member", assign_task),
        ("View Tasks in Project", view_tasks),
        ("View Team Member Workload", view_workload),
        ("Filter by Task Status", filter_tasks),
        ("Check Overdue Tasks", check_overdue),
    ]

    for i, (label, command) in enumerate(actions):
        column = i % 2  # 2 buttons per row
        row = i // 2
        ctk.CTkButton(
            button_frame,
            text=label,
            command=command,
            font=("Helvetica Neue", 16),
            corner_radius=15,
            width=250,
            height=50,
        ).grid(row=row, column=column, padx=30, pady=10)

    # Footer Section
    footer_frame = ctk.CTkFrame(root, height=50, corner_radius=15)
    footer_frame.pack(fill="x", pady=10, side="bottom")
    footer_label = ctk.CTkLabel(
        footer_frame,
        text="Project Management App | Version 1.0 | © 2025",
        font=("Helvetica Neue", 12),
    )
    footer_label.pack(pady=10)

    # Save Projects on Exit
    def on_exit():
        save_projects()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_exit)

    # Run the Application
    root.mainloop()
