class Task:
    def __init__(title, status = 'Not Started', due_date = None, priority = 'Medium', assignee = None):
        self.title = title
        self.status = status
        self.due_date = due_date
        self.priority = priority
        self.assignee = assignee

    def update_status(self, new_status):
        self.status = new_status

    def update_assignee(self, team_member):
        self.assignee = team_member

    def to_dict(self):
        return {
            'title': self.title,
            'status': self.status,
            'due_date': self.due_date,
            'priority': self.priority,
            'assignee': self.assignee.name if self.assignee else None
        }