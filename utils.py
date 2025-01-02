import json
from datetime import datetime

def save_to_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent = 4)

def load_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    

def check_overdue_tasks(projects):
    today = datetime.now().date()
    for project in projects:
        print(f"\nOverdue Tasks in Project: {project.name}")
        
        if not project.tasks:  # Check if the project has no tasks
            print("No tasks in this project.")
            continue  # Skip to the next project

        overdue_found = False  # Flag to track if overdue tasks exist
        for task in project.tasks:
            if task.due_date and datetime.strptime(task.due_date, "%Y-%m-%d").date() < today:
                overdue_found = True
                print(f"- {task.title} (Due: {task.due_date}, Status: {task.status})")

        if not overdue_found:  # If no overdue tasks are found
            print("No overdue tasks in this project.")
