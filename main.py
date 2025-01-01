from project import Project
from task import Task
from team_member import TeamMember
from utils import load_from_json, save_to_json
from utils import check_overdue_tasks

def main():
    print("\n" + "-" * 30)
    print("Project Management App")
    print("-" * 30)

    projects = []

    DATA_FILE = 'example.json'

    # Load data from previous if available
    try:
        project_data = load_from_json(DATA_FILE)
        for proj in project_data:
            project = Project(proj['name'], proj['desc'], proj['deadline'])
            for t in proj['tasks']:
                task = Task(
                    t['title'],
                    status=t['status'],
                    due_date=t['due_date'],
                    priority=t['priority'],
                    assignee=TeamMember(t['assignee']) if t['assignee'] else None
                )
                project.add_task(task)
            projects.append(project)
    except FileNotFoundError:
        print('No saved data found. Starting new.')

    while True:
        print('\n1. Create a Project')
        print('2. Add a task to a project')
        print('3. View All Tasks in a Project')
        print('4. Assign a Task to a Team Member')
        print('5. View Team Member Workload')
        print('6. Filter by category: ')
        print('7. Check overdue tasks')
        print('8. Save and Exit')

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input('Enter project name: ')
            desc = input('Enter project description: ')
            deadline = input('Enter project deadline (YYYY-MM-DD): ')
            projects.append(Project(name, desc, deadline))
            print(f'Project {name} created!')
        
        elif choice == '2':
            if not projects:
                print('No projects available. Create one first.')
                continue
            for i, project in enumerate(projects, 1):
                print(f'{i}. {project.name}')
            try:
                project_choice = int(input('Select a project: ')) - 1
                title = input('Enter task title: ')
                due_date = input("Enter due date (YYYY-MM-DD): ")
                priority = input("Enter priority (High/Medium/Low): ")
                task = Task(title, due_date=due_date, priority=priority)
                projects[project_choice].add_task(task)
                print(f'Task {title} added to project {projects[project_choice].name}!')
            except (ValueError, IndexError):
                print("Invalid project selection. Try again.")

        elif choice == '3':
            if not projects:
                print('No projects available.')
                continue
            for i, project in enumerate(projects, 1):
                print(f'{i}. {project.name}')
            try:
                project_choice = int(input('Select a project: ')) - 1
                selected_project = projects[project_choice]
                print(f'\nTasks for project: {selected_project.name}')
                for task in selected_project.tasks:
                    print(f"- {task.title} (Status: {task.status}, Due: {task.due_date}, Priority: {task.priority})")
            except (ValueError, IndexError):
                print("Invalid project selection. Try again.")

        elif choice == '4':
            if not projects:
                print('No projects available.')
                continue
            for i, project in enumerate(projects, 1):
                print(f"{i}. {project.name}")
            try:
                project_choice = int(input("Select a project: ")) - 1
                selected_project = projects[project_choice]
                for i, task in enumerate(selected_project.tasks, 1):
                    print(f'{i}. {task.title}')
                task_choice = int(input('Select a task: ')) - 1
                task = selected_project.tasks[task_choice]
                assignee_name = input("Enter team member's name: ")
                assignee = TeamMember(assignee_name)
                task.update_assignee(assignee)
                print(f'Task {task.title} assigned to {assignee_name}')
            except (ValueError, IndexError):
                print("Invalid selection. Try again.")

        elif choice == '5':
            member_name = input("Enter team member's name: ")
            member_tasks = []
            for project in projects:
                for task in project.tasks:
                    if task.assignee and task.assignee.name == member_name:
                        member_tasks.append(task.title)
            print(f"\n{member_name}'s Workload:")
            for task_title in member_tasks:
                print(f' - {task_title}')
            if not member_tasks:
                print('No tasks assigned.')

        elif choice == '6':  # New option for filtering tasks
            filter_type = input("Filter by - 1. Status, 2. Priority, 3. Assignee: ")
            if filter_type == '1':
                status_filter = input("Enter status (Not Started/In Progress/Completed): ")
                for project in projects:
                    print(f"\nTasks in Project: {project.name}")
                    for task in project.tasks:
                        if task.status == status_filter:
                            print(f"- {task.title} (Due: {task.due_date}, Priority: {task.priority})")
            elif filter_type == '2':
                priority_filter = input("Enter priority (High/Medium/Low): ")
                for project in projects:
                    print(f"\nTasks in Project: {project.name}")
                    for task in project.tasks:
                        if task.priority == priority_filter:
                            print(f"- {task.title} (Due: {task.due_date}, Priority: {task.priority})")
            elif filter_type == '3':
                assignee_filter = input("Enter assignee name: ")
                for project in projects:
                    print(f"\nTasks in Project: {project.name}")
                    for task in project.tasks:
                        if task.assignee and task.assignee.name == assignee_filter:
                            print(f"- {task.title} (Due: {task.due_date}, Priority: {task.priority})")

        elif choice == '7':  # Example new option
            print("\n--- Checking Overdue Tasks ---")
            check_overdue_tasks(projects)
        
        
        elif choice == '8':
            confirm = input("Are you sure you want to exit? (yes/no): ").lower()
            if confirm == 'yes':
                save_to_json(DATA_FILE, [proj.to_dict() for proj in projects])
                print("Data saved. Exiting...")
                break

        else:
            print('Invalid choice. Please try again.')
                         

if __name__ == "__main__":
    main()
