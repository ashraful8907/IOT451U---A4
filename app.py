import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_analytics_visualisations(parent, projects):
    """
    Displays analytics visualizations (charts and progress bars) in a new window.

    Args:
        parent: The parent widget to attach the visualization window.
        projects: A list of Project objects.
    """
    visualisation_window = ctk.CTkToplevel(parent)
    visualisation_window.title("Analytics Visualisations")
    visualisation_window.geometry("800x600")

    # Frame for Charts
    chart_frame = ctk.CTkFrame(visualisation_window)
    chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Generate Analytics
    _generate_task_completion_chart(chart_frame, projects)
    _generate_workload_distribution_chart(chart_frame, projects)
    _generate_project_progress_bars(visualisation_window, projects)

def _generate_task_completion_chart(parent, projects):
    completed = sum(
        1 for proj in projects for task in proj.tasks if task.status == "Completed"
    )
    pending = sum(
        1 for proj in projects for task in proj.tasks if task.status != "Completed"
    )

    # Create Pie Chart
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie([completed, pending], labels=["Completed", "Pending"], autopct="%1.1f%%", colors=["green", "red"])
    ax.set_title("Task Completion Rate")

    # Embed Chart in GUI
    canvas = FigureCanvasTkAgg(fig, parent)
    canvas.get_tk_widget().pack(side="left", padx=10, pady=10)
    canvas.draw()

def _generate_workload_distribution_chart(parent, projects):
    team_members = {}
    for proj in projects:
        for task in proj.tasks:
            if task.assignee:
                team_members[task.assignee.name] = team_members.get(task.assignee.name, 0) + 1

    members = list(team_members.keys())
    task_counts = list(team_members.values())

    # Create Bar Chart
    fig = Figure(figsize=(4, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(members, task_counts, color="blue")
    ax.set_title("Workload Distribution")
    ax.set_xlabel("Team Members")
    ax.set_ylabel("Number of Tasks")

    # Embed Chart in GUI
    canvas = FigureCanvasTkAgg(fig, parent)
    canvas.get_tk_widget().pack(side="left", padx=10, pady=10)
    canvas.draw()

def _generate_project_progress_bars(parent, projects):
    # Frame for Progress Bars
    progress_frame = ctk.CTkFrame(parent)
    progress_frame.pack(fill="both", expand=True, padx=10, pady=10)

    for project in projects:
        project_name = project.name
        total_tasks = len(project.tasks)
        completed_tasks = sum(1 for task in project.tasks if task.status == "Completed")
        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        # Progress Bar Label
        label = ctk.CTkLabel(progress_frame, text=f"{project_name} Progress")
        label.pack(anchor="w", pady=5)

        # Progress Bar
        progress_bar = ctk.CTkProgressBar(progress_frame)
        progress_bar.set(progress / 100)  # Set progress (0 to 1)
        progress_bar.pack(fill="x", pady=5)

# Example Usage
if __name__ == "__main__":
    from classes import Project, Task, TeamMember

    app = ctk.CTk()
    app.geometry("800x600")

    # Mock Projects Data
    task1 = Task("Task 1", "Description", "2025-01-15", "High")
    task1.status = "Completed"
    task2 = Task("Task 2", "Description", "2025-01-16", "Medium")
    task2.assignee = TeamMember("Alice", "Developer", "Assigned")

    project1 = Project("Project Alpha", "Description", "2025-02-01")
    project1.add_task(task1)
    project1.add_task(task2)

    projects = [project1]

    ctk.CTkButton(
        app,
        text="Show Visualisations",
        command=lambda: show_analytics_visualisations(app, projects),
        width=300,
        height=50,
    ).pack(pady=20)

    app.mainloop()
