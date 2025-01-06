from datetime import datetime

# Base Class that the others will inherit from
class BaseEntity:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def display_details(self):
        raise NotImplementedError("Subclasses must implement this method.")

class Task(BaseEntity):
    def __init__(self, name, description, due_date, assignee=None, status="Not Started", priority='Medium'):
        super().__init__(name, description)
        self.__due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.assignee = assignee
        self.status = status
        self.priority = priority

    @property
    def due_date(self):
        return self.__due_date

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value in ["Not Started", "In Progress", "Completed"]:
            self.__status = value
        else:
            raise ValueError("Invalid status. Use 'Not Started', 'In Progress', or 'Completed'.")

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value):
        if value in ["Low", "Medium", "High"]:
            self.__priority = value
        else:
            raise ValueError("Invalid priority. Use 'Low', 'Medium', or 'High'.")

    def display_details(self):
        return (f"Task: {self.name}\n"
                f"Description: {self.description}\n"
                f"Due Date: {self.__due_date.strftime('%Y-%m-%d')}\n"
                f"Assignee: {self.assignee.name if self.assignee else 'Unassigned'}\n"
                f"Status: {self.status}\n"
                f"Priority: {self.priority}\n")

    def to_dict(self):
        return {
            "title": self.name,
            "description": self.description,
            "due_date": self.__due_date.strftime("%Y-%m-%d"),
            "assignee": self.assignee.name if self.assignee else None,
            "status": self.status,
            "priority": self.priority,
        }

class Project(BaseEntity):
    def __init__(self, name, description, deadline):
        super().__init__(name, description)
        self.__deadline = datetime.strptime(deadline, "%Y-%m-%d")
        self.__tasks = []

    @property
    def deadline(self):
        return self.__deadline

    @property
    def tasks(self):
        return self.__tasks

    def add_task(self, task):
        if isinstance(task, Task):
            self.__tasks.append(task)
        else:
            raise ValueError("Only Task instances can be added.")

    def remove_task(self, task_name):
        self.__tasks = [task for task in self.__tasks if task.name != task_name]

    def display_details(self):
        task_list = "\n".join([task.name for task in self.__tasks])
        return (f"Project: {self.name}\n"
                f"Description: {self.description}\n"
                f"Deadline: {self.__deadline.strftime('%Y-%m-%d')}\n"
                f"Tasks:\n{task_list}\n")

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "tasks": [task.to_dict() for task in self.__tasks],
        }

class TeamMember(BaseEntity):
    def __init__(self, name, description, role):
        super().__init__(name, description)
        self.role = role
        self.__tasks = []

    def assign_task(self, task):
        if isinstance(task, Task):
            self.__tasks.append(task)
        else:
            raise ValueError("Only Task instances can be assigned.")

    def display_details(self):
        task_list = "\n".join([task.name for task in self.__tasks])
        return (f"Team Member: {self.name}\n"
                f"Role: {self.role}\n"
                f"Description: {self.description}\n"
                f"Assigned Tasks:\n{task_list}\n")
