import customtkinter as ctk
from tkinter import messagebox, Toplevel
from classes import Project, Task, TeamMember
from datetime import datetime
from app import show_analytics_visualisations

ctk.set_widget_scaling(1.0)  # Disable widget DPI scaling
ctk.set_window_scaling(1.0)  # Disable window DPI scaling

# Main GUI Function
def main_window(projects, save_projects):
    # Initialise Application
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Project Management App")
    root.geometry("1000x700")

     # Statistics Label
    stats_label = ctk.CTkLabel(root, text="")
    stats_label.pack(pady=10)

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
            deadline_date = project_deadline_entry.get()
            if not name or not deadline_date:
                messagebox.showerror("Error", "Project name and deadline are required.")
                return
            try:
                deadline_str = deadline_date if isinstance(deadline_date, str) else deadline_date.strftime("%Y-%m-%d")
                deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return
            new_project = Project(name, description, deadline_str)
            projects.append(new_project)
            update_stats()
            new_project_window.destroy()
            messagebox.showinfo("Success", f"Project {name} created!")

        new_project_window = Toplevel(root)
        new_project_window.title("Create New Project")
        new_project_window.geometry("400x400")

        project_name_label = ctk.CTkLabel(new_project_window, text="Project Name:", text_color="black")
        project_name_label.pack(pady=5)
        project_name_entry = ctk.CTkEntry(new_project_window)
        project_name_entry.pack(pady=5)

        project_desc_label = ctk.CTkLabel(new_project_window, text="Project Description:", text_color="black")
        project_desc_label.pack(pady=5)
        project_desc_entry = ctk.CTkEntry(new_project_window)
        project_desc_entry.pack(pady=5)

        project_deadline_label = ctk.CTkLabel(new_project_window, text="Project Deadline (YYYY-MM-DD):", text_color="black")
        project_deadline_label.pack(pady=5)
        project_deadline_entry = ctk.CTkEntry(new_project_window)
        project_deadline_entry.pack(pady=5)

        save_button = ctk.CTkButton(new_project_window, text="Save Project", command=save_new_project)
        save_button.pack(pady=20)

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
        add_task_window.geometry("600x500")

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
        def save_assignee():
            assignee_name = assignee_entry.get()
            project_name = project_dropdown.get()
            task_name = task_dropdown.get()

            if not project_name or not task_name:
                messagebox.showerror("Error", "Please select a project and task.")
                return

            selected_project = next((proj for proj in projects if proj.name == project_name), None)
            selected_task = next((task for task in selected_project.tasks if task.name == task_name), None)

            if not selected_task:
                messagebox.showerror("Error", "Selected task not found.")
                return

            selected_task.assignee = TeamMember(name=assignee_name, description="", role="Assigned")
            messagebox.showinfo("Success", f"Task '{task_name}' assigned to {assignee_name}.")
            assign_window.destroy()

        def update_tasks(selected_project_name):
            """Update the task dropdown based on the selected project."""
            selected_project = next((proj for proj in projects if proj.name == selected_project_name), None)

            if selected_project and selected_project.tasks:
                task_names = [task.name for task in selected_project.tasks]
                task_dropdown.configure(values=task_names)
                task_dropdown.set("")
            else:
                task_dropdown.configure(values=["No tasks available"])
                task_dropdown.set("No tasks available")

        assign_window = Toplevel(root)
        assign_window.title("Assign Task")
        assign_window.geometry("500x500")

        # Project Dropdown
        ctk.CTkLabel(assign_window, text="Select Project", text_color="black").pack(pady=10)
        project_dropdown = ctk.CTkComboBox(
            assign_window,
            values=[proj.name for proj in projects],
            command=update_tasks,  # Call update_tasks when a project is selected
        )
        project_dropdown.pack(pady=5)

        # Task Dropdown
        ctk.CTkLabel(assign_window, text="Select Task", text_color="black").pack(pady=10)
        task_dropdown = ctk.CTkComboBox(assign_window, values=[])
        task_dropdown.pack(pady=5)

        # Assignee Entry
        ctk.CTkLabel(assign_window, text="Assign Team Member", text_color="black").pack(pady=10)
        assignee_entry = ctk.CTkEntry(assign_window)
        assignee_entry.pack(pady=5)

        # Assign Button
        ctk.CTkButton(assign_window, text="Assign Task", command=save_assignee).pack(pady=20)

        # Initialise the first project selection and its tasks
        if projects:
            first_project_name = projects[0].name
            project_dropdown.set(first_project_name)
            update_tasks(first_project_name)

    def view_tasks(root, projects):
        """Display tasks grouped by project with collapsible sections."""
        tasks_window = Toplevel(root)
        tasks_window.title("View Tasks")
        tasks_window.geometry("600x800")

        for project in projects:
            project_frame = ctk.CTkFrame(tasks_window, corner_radius=10)
            project_frame.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(
                project_frame, text=f"Project: {project.name}", font=("Helvetica Neue", 16, "bold"), text_color="white"
            ).pack(anchor="w", padx=10, pady=5)

            task_frame = ctk.CTkFrame(project_frame, fg_color="transparent")
            [ctk.CTkLabel(task_frame, text=f"  - {task.name or 'Unnamed Task'} | Status: {task.status} | Due: {task.due_date} | Priority: {task.priority}", font=("Helvetica Neue", 12), text_color="white").pack(anchor="w", padx=10) for task in project.tasks]
            task_frame.pack_forget()

            ctk.CTkButton(
                project_frame, text="Show Tasks",
                command=lambda f=task_frame: f.pack(fill="x", padx=10, pady=5) if not f.winfo_ismapped() else f.pack_forget(),
                width=100, height=30
            ).pack(anchor="e", padx=10, pady=5)


    def view_workload(root, projects):
        """Display workload for all team members in a collapsible format."""
        workload_window = Toplevel(root)
        workload_window.title("Team Member Workload")
        workload_window.geometry("600x600")

        # Dictionary to track tasks grouped by team members
        member_workload = {}

        # Collect all tasks and group them by team member
        for proj in projects:
            for task in proj.tasks:
                if task.assignee and task.assignee.name:  # Ensure task has a valid assignee
                    if task.assignee.name not in member_workload:
                        member_workload[task.assignee.name] = []
                    member_workload[task.assignee.name].append(f"{task.name} (Project: {proj.name})")

        # Handle case where no tasks are assigned
        if not member_workload:
            ctk.CTkLabel(
                workload_window,
                text="No tasks assigned to any team members.",
                font=("Helvetica Neue", 16),
                text_color="black"
            ).pack(pady=20)
            return

        # Create collapsible sections for each team member
        for member, tasks in member_workload.items():
            # Frame for each team member
            member_frame = ctk.CTkFrame(workload_window, corner_radius=10)
            member_frame.pack(fill="x", padx=10, pady=5)

            # Header for the team member
            header = ctk.CTkLabel(
                member_frame,
                text=f"{member} ({len(tasks)} tasks)",
                font=("Helvetica Neue", 16, "bold"),
                text_color="white"
            )
            header.pack(anchor="w", padx=10, pady=5)

            # Task list frame (hidden by default)
            task_frame = ctk.CTkFrame(member_frame, fg_color="transparent")
            task_frame.pack(fill="x", padx=10, pady=5)

            # Populate tasks
            for task in tasks:
                ctk.CTkLabel(
                    task_frame,
                    text=f"  - {task}",
                    font=("Helvetica Neue", 12),
                    text_color="white"
                ).pack(anchor="w", padx=10)

            # Initially hide the tasks
            task_frame.pack_forget()

            # Toggle button to show/hide tasks
            def toggle_tasks(frame=task_frame):
                if frame.winfo_ismapped():
                    frame.pack_forget()
                else:
                    frame.pack(fill="x", padx=10, pady=5)

            toggle_button = ctk.CTkButton(
                member_frame,
                text="Show Tasks",
                command=toggle_tasks,
                width=100,
                height=30,
            )
            toggle_button.pack(anchor="e", padx=10, pady=5)





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
        view_window.geometry("")
        
        if not projects:
            ctk.CTkLabel(view_window, text="No projects available.", font=("Helvetica Neue", 16), text_color= "black").pack(pady=20)
            return

        for proj in projects:
            project_label = ctk.CTkLabel(
                view_window,
                text_color="black",
                text=f"Project: {proj.name} | Description: {proj.description} | Deadline: {proj.deadline.strftime('%Y-%m-%d')}",
                font=("Helvetica Neue", 16, "bold"),
                anchor="center",
                justify='center',
                wraplength=550,
            )
            project_label.pack(pady=10, anchor="center")

            if proj.tasks:
                task_label = ctk.CTkLabel(view_window, text="Tasks:", font=("Helvetica Neue", 14, "bold"), text_color= "black")
                task_label.pack(anchor="w")
                for task in proj.tasks:
                    task_info = f"  - {task.name} | Status: {task.status} | Priority: {task.priority} | Due: {task.due_date.strftime('%Y-%m-%d')}"
                    task_item = ctk.CTkLabel(view_window, text=task_info, font=("Helvetica Neue", 12), justify="left", anchor="w", text_color= "black")
                    task_item.pack(anchor="w")
            else:
                no_tasks_label = ctk.CTkLabel(view_window, text="  No tasks added yet.", font=("Helvetica Neue", 12), text_color= "black")
                no_tasks_label.pack(anchor="center")
    
    def remove_task():
        def delete_task():
            project_name = project_dropdown.get()
            task_name = task_dropdown.get()

            if not project_name or not task_name:
                messagebox.showerror("Error", "Please select a project and task.")
                return

            selected_project = next((proj for proj in projects if proj.name == project_name), None)
            if not selected_project:
                messagebox.showerror("Error", f"Project '{project_name}' not found.")
                return

            selected_task = next((task for task in selected_project.tasks if task.name == task_name), None)
            if not selected_task:
                messagebox.showerror("Error", f"Task '{task_name}' not found.")
                return

            selected_project.remove_task(task_name)
            messagebox.showinfo("Success", f"Task '{task_name}' removed.")
            save_projects()
            remove_window.destroy()

        def update_tasks(selected_project_name):
            selected_project = next((proj for proj in projects if proj.name == selected_project_name), None)

            if selected_project and selected_project.tasks:
                task_names = [task.name for task in selected_project.tasks]
                task_dropdown.configure(values=task_names)
                task_dropdown.set("")
            else:
                task_dropdown.configure(values=["No tasks available"])
                task_dropdown.set("No tasks available")

        remove_window = Toplevel(root)
        remove_window.title("Remove Task")
        remove_window.geometry("500x400")

        # Project Dropdown
        ctk.CTkLabel(remove_window, text="Select Project", text_color="black").pack(pady=10)
        project_dropdown = ctk.CTkComboBox(
            remove_window,
            values=[proj.name for proj in projects],
            command=update_tasks,
        )
        project_dropdown.pack(pady=5)

        # Task Dropdown
        ctk.CTkLabel(remove_window, text="Select Task", text_color="black").pack(pady=10)
        task_dropdown = ctk.CTkComboBox(remove_window, values=[])
        task_dropdown.pack(pady=5)

        # Remove Button
        ctk.CTkButton(remove_window, text="Remove Task", command=delete_task, fg_color="#FF3B30").pack(pady=20)

        # Initialise the first project selection and its tasks
        if projects:
            first_project_name = projects[0].name
            project_dropdown.set(first_project_name)
            update_tasks(first_project_name)


    def complete_task():
        def mark_completed():
            project_name = project_dropdown.get()
            task_name = task_dropdown.get()

            if not project_name or not task_name:
                messagebox.showerror("Error", "Please select a project and task.")
                return

            selected_project = next((proj for proj in projects if proj.name == project_name), None)
            if not selected_project:
                messagebox.showerror("Error", f"Project '{project_name}' not found.")
                return

            selected_task = next((task for task in selected_project.tasks if task.name == task_name), None)
            if not selected_task:
                messagebox.showerror("Error", f"Task '{task_name}' not found.")
                return

            selected_task.status = "Completed"
            messagebox.showinfo("Success", f"Task '{task_name}' marked as completed.")
            save_projects()
            complete_window.destroy()

        def update_tasks(selected_project_name):
            selected_project = next((proj for proj in projects if proj.name == selected_project_name), None)

            if selected_project and selected_project.tasks:
                task_names = [task.name for task in selected_project.tasks]
                task_dropdown.configure(values=task_names)
                task_dropdown.set("")
            else:
                task_dropdown.configure(values=["No tasks available"])
                task_dropdown.set("No tasks available")

        complete_window = Toplevel(root)
        complete_window.title("Complete Task")
        complete_window.geometry("500x400")

        # Label and Dropdown for Project
        ctk.CTkLabel(complete_window, text="Select Project:", text_color="black").pack(pady=10)
        project_dropdown = ctk.CTkComboBox(
            complete_window,
            values=[proj.name for proj in projects],
            command=update_tasks,
        )
        project_dropdown.pack(pady=5)

        # Label and Dropdown for Task
        ctk.CTkLabel(complete_window, text="Select Task:", text_color="black").pack(pady=10)
        task_dropdown = ctk.CTkComboBox(complete_window, values=[])
        task_dropdown.pack(pady=5)

        # Complete Button with Green Color
        ctk.CTkButton(
            complete_window,
            text="Complete Task",
            command=mark_completed,
            fg_color="#4CD964",  # Set the button's color to green
        ).pack(pady=20)

        # Initialise the first project selection and its tasks
        if projects:
            first_project_name = projects[0].name
            project_dropdown.set(first_project_name)
            update_tasks(first_project_name)

        ctk.CTkButton(
            button_frame,
            text="Show Dashboard",
            command=lambda: show_dashboard(root, [proj.to_dict() for proj in projects]),
            font=("Helvetica Neue", 16),
            corner_radius=15,
            width=250,
            height=50,
        ).grid(row=row, column=column, padx=30, pady=10)

    def show_dashboard():
        dashboard_window = ctk.CTkToplevel(root)
        dashboard_window.title("Analytics Dashboard")
        dashboard_window.geometry("800x600")

        # Create and pack the Analytics Dashboard
        dashboard = show_analytics_visualisations(dashboard_window, projects)
        dashboard.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkButton(
    root,
    text="Show Visualisations",
    font=("Helvetica Neue", 16),
    command=lambda: show_analytics_visualisations(root, projects),
    width=300,
    height=50,
    ).pack(pady=20)


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
        ("View Tasks in Project", lambda: view_tasks(root, projects)),
        ("View Team Member Workload", lambda: view_workload(root, projects)),
        ("Filter by Task Status", filter_tasks),
        ("Check Overdue Tasks", check_overdue),
        ("Complete Task", complete_task),
        ("Remove Task", remove_task),
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

    after_callbacks = []  # Track scheduled callbacks

    def some_function():
        """Periodic function for updating stats."""
        if not root.winfo_exists():  # Check if root exists
            return
        update_stats()
        callback_id = root.after(1000, some_function)
        after_callbacks.append(callback_id)

    # Start periodic updates
    callback_id = root.after(1000, some_function)
    after_callbacks.append(callback_id)

    def on_exit():
        # Save data and destroy window
        save_projects()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_exit)

    update_stats()

    try:
        root.mainloop()
    except Exception as e:
        print(f"Unhandled exception: {e}")


