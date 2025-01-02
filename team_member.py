class TeamMember:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def assign_task(self, task):
        self.tasks.append(task)
    
    def get_workload(self):
        return len(self.tasks)
    
    def to_dict(self):
        return {
            'name' : self.name,
            'tasks' : [tasks.todict() for task in self.tasks]
        }