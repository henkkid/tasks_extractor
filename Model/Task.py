from Model.Event import Event

class Task:
        
    def __init__(self, context, events=None):
        self.context = context
        self.events = events if events is not None else []

    #declare all attributes of a task object
    task_id = 0
    task_subject = ""
    task_tender_price = 0
    task_estimatedtime = 0
    task_start_datetime = ""
    task_end_datetime = ""
    tasks_createdate = ""
    task_deadline = ""
    task_scrum_value = ""
    task_scrum_effort = ""
    employee = ""
    project = 0
    sprint = 0
    reference = ""
    type = ""
    status = ""
    priority = ""
    events = []
    total_time_of_events_in_minutes = 0
    total_time_of_events_in_hours = 0
    
    def addEvent(self, event):
        self.events.append(event)

    def calculateTotalTimeOfEvents(self):
        for event in self.events:
            self.total_time_of_events_in_minutes += event.time_in_minutes
        self.total_time_of_events_in_hours = round(self.total_time_of_events_in_minutes / 60, 2)
        
    
    def __str__(self):
        string = f"Task ID: {self.task_id} Task Subject: {self.task_subject} \n"
        number_of_events = len(self.events)
        string += f"number of events: {number_of_events} \n"
        string += f"type of task: {self.type} \n"
        string += f"create date: {self.tasks_createdate} \n"
        string += f"total time of events in minutes: {self.total_time_of_events_in_minutes} \n"
        string += f"total time of events in hours: {self.total_time_of_events_in_hours} \n"
        for event in self.events:
           string += f"{event} \n"
        
        string += "------------------------------------ \n"

        return string