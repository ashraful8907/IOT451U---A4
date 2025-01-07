from classes import Project, Task, TeamMember

# Mock data
projects = []

# Add a project
test_project = Project(name="Test", description="Test Description", deadline="2025-05-12")
projects.append(test_project)

# Add tasks to the project
test_task_1 = Task(name="Task 1", description="Important Task 1", due_date="2025-01-01", priority="High")
test_task_2 = Task(name="Task 2", description="Important Task 2", due_date="2025-01-15", priority="Medium")
test_project.add_task(test_task_1)
test_project.add_task(test_task_2)

# Function to simulate Assign Task to Team Member
def test_assign_task(selected_project_name, selected_task_name, assignee_name):
    """Simulate assigning a task to a team member and output debug info."""
    print(f"Selected Project: {selected_project_name}")
    selected_project = next((proj for proj in projects if proj.name == selected_project_name), None)
    
    if not selected_project:
        print(f"Error: Project '{selected_project_name}' not found.")
        return

    print(f"Found Project: {selected_project.name}")
    print(f"Tasks in Project: {[task.name for task in selected_project.tasks]}")

    selected_task = next((task for task in selected_project.tasks if task.name == selected_task_name), None)
    if not selected_task:
        print(f"Error: Task '{selected_task_name}' not found in project '{selected_project_name}'.")
        return

    print(f"Found Task: {selected_task.name}")
    selected_task.assignee = TeamMember(name=assignee_name, description="", role="Assigned")
    print(f"Success: Task '{selected_task.name}' assigned to {selected_task.assignee.name}.")

# Test case
print("===== Running Test =====")
test_assign_task(selected_project_name="Test", selected_task_name="Task 1", assignee_name="John Doe")
print("========================")
