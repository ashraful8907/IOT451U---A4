# main.py
from classes import Task, Project, TeamMember
from utils import load_from_json, save_to_json
import os
from GUI import main_window
import customtkinter as ctk

# Set scaling for customtkinter widgets and windows
ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)

# Global Variables
projects = []  # List to store project instances
data_file = os.path.join(os.path.dirname(__file__), 'mock.json')  # Data file path

# Function to Load Projects from File
def load_projects(data_file):
    global projects
    projects = []  # Reset projects list
    try:
        if not os.path.exists(data_file):
            print(f"File {data_file} does not exist. Creating a new file.")
            save_to_json(data_file, [])  # Create an empty JSON file

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
        print(f"Loaded {len(projects)} projects from {data_file}.")
    except Exception as e:
        print(f"Error loading projects: {e}")

# Function to Save Projects to File
def save_projects():
    try:
        if not projects:
            print("No projects to save. Skipping save operation.")
            return
        save_to_json(data_file, [proj.to_dict() for proj in projects])
        print(f"Saved {len(projects)} projects to {data_file}.")
    except Exception as e:
        print(f"Error saving projects: {e}")

# Main Function
if __name__ == "__main__":
    load_projects(data_file)
    main_window(projects, save_projects)
