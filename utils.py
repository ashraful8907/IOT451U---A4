import json
from datetime import datetime

def save_to_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent = 4)

def load_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    
from datetime import datetime

def check_overdue_tasks(projects):
    """Checks for overdue tasks in all projects."""
    overdue_tasks = []
    today = datetime.now().date()  # Current date

    for project in projects:
        for task in project.tasks:
            # Check if due_date is before today and task is not completed
            if task.due_date.date() < today and task.status != "Completed":
                overdue_tasks.append(f"{task.name} (Due: {task.due_date.strftime('%Y-%m-%d')})")

    return overdue_tasks

