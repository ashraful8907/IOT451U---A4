import unittest
from datetime import datetime
from classes import Task, Project, TeamMember
from main import load_projects
import os
import json

class TestProjectManagement(unittest.TestCase):

    def setUp(self):
        # Setup mock data for testing
        self.task1 = Task("Task 1", "Description 1", "2025-01-15", None, "Not Started", "High")
        self.task2 = Task("Task 2", "Description 2", "2025-01-20", None, "Completed", "Medium")
        self.member = TeamMember("Alice", "Developer", "Development")

        self.project = Project("Project Alpha", "A test project", "2025-02-01")
        self.project.add_task(self.task1)
        self.project.add_task(self.task2)

        self.data_file = "test_data.json"

    def tearDown(self):
        # Clean up mock data file after tests
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

    def test_task_creation(self):
        self.assertEqual(self.task1.name, "Task 1")
        self.assertEqual(self.task1.due_date, datetime.strptime("2025-01-15", "%Y-%m-%d"))
        self.assertEqual(self.task1.status, "Not Started")

    def test_task_priority_validation(self):
        with self.assertRaises(ValueError):
            self.task1.priority = "Critical"

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Project Alpha")
        self.assertEqual(len(self.project.tasks), 2)

    def test_add_task_to_project(self):
        new_task = Task("Task 3", "Description 3", "2025-01-25", None, "Not Started", "Low")
        self.project.add_task(new_task)
        self.assertEqual(len(self.project.tasks), 3)

    def test_remove_task_from_project(self):
        self.project.remove_task("Task 1")
        self.assertEqual(len(self.project.tasks), 1)
        self.assertEqual(self.project.tasks[0].name, "Task 2")

    def test_assign_task_to_member(self):
        self.task1.assignee = self.member
        self.assertEqual(self.task1.assignee.name, "Alice")

    def test_team_member_task_assignment(self):
        self.member.assign_task(self.task1)
        self.assertEqual(len(self.member._TeamMember__tasks), 1)
        self.assertEqual(self.member._TeamMember__tasks[0].name, "Task 1")

    def test_load_projects(self):
        # Mock project data
        mock_data = [
            {
                "name": "Project Alpha",
                "description": "A test project",
                "deadline": "2025-02-01",
                "tasks": [
                    {
                        "title": "Task 1",
                        "description": "Description 1",
                        "due_date": "2025-01-15",
                        "priority": "High",
                        "status": "Not Started",
                        "assignee": None
                    },
                    {
                        "title": "Task 2",
                        "description": "Description 2",
                        "due_date": "2025-01-20",
                        "priority": "Medium",
                        "status": "Completed",
                        "assignee": None
                    }
                ]
            }
        ]

        # Write mock data to file
        with open(self.data_file, "w") as file:
            json.dump(mock_data, file)

        # Call the function to test
        projects = load_projects(self.data_file)

        # Check loaded data
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].name, "Project Alpha")

# Helper function for saving projects in tests
def save_projects_to_test_file(project, file_path):
    data = [project.to_dict()]
    with open(file_path, "w") as file:
        json.dump(data, file)

# Run the tests
if __name__ == "__main__":
    unittest.main()
