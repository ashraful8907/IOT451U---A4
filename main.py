'''
Note to self:
Where to start on Sunday (or Saturday if you're that cool and bothered),
- Issue with loading and saving data, saving into wrong place, not loading old data
- Improve layout and presentation of the GUI with Tkinter - is it even possible to make it look nice - probably search it up.
- Add tests into the code to make sure it works
'''
from project import Project  # Importing the Project class
from task import Task  # Importing the Task class
from team_member import TeamMember  # Importing the TeamMember class
from utils import load_from_json, save_to_json  # Utility functions for file I/O
from utils import check_overdue_tasks  # Utility function for overdue task checking
import tkinter as tk
from tkinter import ttk, messagebox
from GUI import main_window
import os

projects = []  # List to store project instances
data_file = os.path.join(os.path.dirname(__file__), 'example.json')  # File name for saving/loading data 

 # Load data from previous session if available
def load_projects(data_file):
    global projects
    try:
        project_data = load_from_json(data_file)  # Load JSON data
        for proj in project_data:
            # Handle missing 'desc' and other fields gracefully
            name = proj.get('name', 'Unnamed Project')
            desc = proj.get('desc', 'No description provided')  # Default description
            deadline = proj.get('deadline', 'No deadline')  # Default deadline if missing
            
            # Create a Project object
            project = Project(name, desc, deadline)
            
            for t in proj.get('tasks', []):  # Iterate over tasks
                # Create Task objects with default values for missing fields
                task = Task(
                    t.get('title', 'Unnamed Task'),
                    status=t.get('status', 'Not Started'),
                    due_date=t.get('due_date', None),
                    priority=t.get('priority', 'Medium'),
                    assignee=TeamMember(t['assignee']) if t.get('assignee') else None
                )
                project.add_task(task)  # Add task to the project
            
            projects.append(project)  # Add project to the list
    except FileNotFoundError:
        print('No saved data found. Starting new.')
    except (KeyError, ValueError) as e:
        print(f"Error loading data: {e}")
    return projects

def save_projects():
    save_to_json(data_file, [proj.to_dict() for proj in projects])
    print("Data saved successfully.")

def main():
    # Displaying the application title and menu
    print("\n" + "-" * 30)
    print("Project Management App")
    print("-" * 30)

    projects = load_projects(data_file)  # Load projects at the start

    # Main loop for user interaction
    while True:
        # Displaying menu options
        print('\n1. Create a Project')
        print('2. Add a task to a project')
        print('3. View All Tasks in a Project')
        print('4. Assign a Task to a Team Member')
        print('5. View Team Member Workload')
        print('6. Filter by category: ')
        print('7. Check overdue tasks')
        print('8. Save and Exit')

        choice = input("Enter your choice: ")  # User input for menu choice

        if choice == '1':  # Option to create a project
            name = input('Enter project name: ')  # Input project details
            desc = input('Enter project description: ')
            deadline = input('Enter project deadline (YYYY-MM-DD): ')
            projects.append(Project(name, desc, deadline))  # Create and add project
            print(f'Project {name} created!')

        elif choice == '2':  # Option to add a task
            if not projects:
                print('No projects available. Create one first.')  # Validation for no projects
                continue
            # Display available projects
            for i, project in enumerate(projects, 1):
                print(f'{i}. {project.name}')
            try:
                project_choice = int(input('Select a project: ')) - 1  # Select project
                title = input('Enter task title: ')  # Input task details
                due_date = input("Enter due date (YYYY-MM-DD): ")
                priority = input("Enter priority (High/Medium/Low): ")
                task = Task(title, due_date=due_date, priority=priority)  # Create task instance
                projects[project_choice].add_task(task)  # Add task to selected project
                print(f'Task {title} added to project {projects[project_choice].name}!')
            except (ValueError, IndexError):
                print("Invalid project selection. Try again.")  # Error handling for invalid input

        elif choice == '3':  # Option to view tasks in a project
            if not projects:
                print('No projects available.')  # Validation for no projects
                continue
            # Display available projects
            for i, project in enumerate(projects, 1):
                print(f'{i}. {project.name}')
            try:
                project_choice = int(input('Select a project: ')) - 1  # Select project
                selected_project = projects[project_choice]  # Retrieve selected project
                print(f'\nTasks for project: {selected_project.name}')
                for task in selected_project.tasks:  # List tasks in the project
                    print(f"- {task.title} (Status: {task.status}, Due: {task.due_date}, Priority: {task.priority})")
            except (ValueError, IndexError):
                print("Invalid project selection. Try again.")  # Error handling for invalid input

        elif choice == '4':  # Option to assign a task
            if not projects:
                print('No projects available.')  # Validation for no projects
                continue
            # Display available projects
            for i, project in enumerate(projects, 1):
                print(f"{i}. {project.name}")
            try:
                project_choice = int(input("Select a project: ")) - 1  # Select project
                selected_project = projects[project_choice]  # Retrieve selected project
                # List tasks in the selected project
                for i, task in enumerate(selected_project.tasks, 1):
                    print(f'{i}. {task.title}')
                task_choice = int(input('Select a task: ')) - 1  # Select task
                task = selected_project.tasks[task_choice]  # Retrieve selected task
                assignee_name = input("Enter team member's name: ")  # Input assignee name
                assignee = TeamMember(assignee_name)  # Create assignee instance
                task.update_assignee(assignee)  # Update task with assignee
                print(f'Task {task.title} assigned to {assignee_name}')
            except (ValueError, IndexError):
                print("Invalid selection. Try again.")  # Error handling for invalid input

        elif choice == '5':  # Option to view workload of a team member
            member_name = input("Enter team member's name: ")  # Input team member name
            member_tasks = []  # List to store assigned tasks
            for project in projects:  # Iterate over all projects and tasks
                for task in project.tasks:
                    if task.assignee and task.assignee.name == member_name:  # Match assignee name
                        member_tasks.append(task.title)
            print(f"\n{member_name}'s Workload:")  # Display workload
            for task_title in member_tasks:
                print(f' - {task_title}')
            if not member_tasks:
                print('No tasks assigned.')  # Validation for no assigned tasks

        elif choice == '6':  # Option to filter tasks by category
            filter_type = input("Filter by - 1. Status, 2. Priority, 3. Assignee: ")  # Filter type input
            if filter_type == '1':  # Filter by status
                status_filter = input("Enter status (Not Started/In Progress/Completed): ")
                for project in projects:
                    print(f"\nTasks in Project: {project.name}")
                    for task in project.tasks:
                        if task.status == status_filter:  # Match status
                            print(f"- {task.title} (Due: {task.due_date}, Priority: {task.priority})")
            elif filter_type == '2':  # Filter by priority
                priority_filter = input("Enter priority (High/Medium/Low): ")
                for project in projects:
                    print(f"\nTasks in Project: {project.name}")
                    for task in project.tasks:
                        if task.priority == priority_filter:  # Match priority
                            print(f"- {task.title} (Due: {task.due_date}, Priority: {task.priority})")
            elif filter_type == '3':  # Filter by assignee
                assignee_filter = input("Enter assignee name: ")
                for project in projects:
                    print(f"\nTasks in Project: {project.name}")
                    for task in project.tasks:
                        if task.assignee and task.assignee.name == assignee_filter:  # Match assignee
                            print(f"- {task.title} (Due: {task.due_date}, Priority: {task.priority})")

        elif choice == '7':  # Option to check overdue tasks
            print("\n--- Checking Overdue Tasks ---")
            check_overdue_tasks(projects)  # Call utility function to check overdue tasks

        elif choice == '8':  # Option to save and exit
            confirm = input("Are you sure you want to exit? (yes/no): ").lower()
            if confirm == 'yes':
                # Save data to JSON file
                save_to_json(data_file, [proj.to_dict() for proj in projects])
                print("Data saved. Exiting...")
                break  # Exit the loop and end program

        else:
            print('Invalid choice. Please try again.')  # Handle invalid menu choice


print(f"Data file path: {data_file}")

if __name__ == "__main__":
    load_projects(data_file)
    main_window(projects, save_projects)
