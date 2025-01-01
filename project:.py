class Project: 
    def __init__(self, name, description, deadline, status = 'Not Started'):
        self.name = name 
        self.description = description
        self.deadline = deadline
        self.tasks = []
        self.status = status

    def add_task(self, task):
        self.tasks.append(task)
    
    def remove_task(self, task_title):
        self.tasks = [task for task in self.tasks if task.title != task_title]

    def get_summary(self):
        completed = sum(1 for task in self.tasks if task.status == "Completed")
        total = len(self.tasks)
        return f"{completed}/{total} tasks completed"
