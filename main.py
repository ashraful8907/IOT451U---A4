# main.py #focus on the assign window thar doesnt resize.
from classes import Task, Project, TeamMember
from utils import load_from_json, save_to_json  # Utility functions for file I/O
import os
from GUI import main_window  # Import the GUI function

'''
To dos:
- Fix stats number
- Fix update_tasks
'''

# Global Variables
projects = []  # List to store project instances
data_file = os.path.join(os.path.dirname(__file__), 'example.json')  # Data file path

# Function to Load Projects from File
def load_projects(data_file):
    global projects
    try:
        project_data = load_from_json(data_file)
        for proj in project_data:
            project = Project(
                name=proj.get('name', 'Unnamed Project'),
                description=proj.get('description', 'No description'),
                deadline=proj.get('deadline', '1970-01-01'),
            )
            for t in proj.get('tasks', []):
                task = Task(
                    name=t.get('title', 'Unnamed Task'),
                    description=t.get('description', 'No description provided'),
                    due_date=t.get('due_date', '1970-01-01'),
                    priority=t.get('priority', 'Medium'),
                    status=t.get('status', 'Not Started'),
                    assignee=TeamMember(name=t['assignee'], description='', role='') if t.get('assignee') else None,
                )
                project.add_task(task)
            projects.append(project)
    except FileNotFoundError:
        print("No saved data found. Starting fresh.")
    except (KeyError, ValueError) as e:
        print(f"Error loading data: {e}")

# Function to Save Projects to File
def save_projects():
    save_to_json(data_file, [proj.to_dict() for proj in projects])
    print("Data saved successfully.")

# Main Function
if __name__ == "__main__":
    load_projects(data_file)
    main_window(projects, save_projects)
