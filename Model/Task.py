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
    task_createdate = ""
    task_deadline = ""
    task_scrum_value = ""
    task_scrum_effort = ""
    employee = ""
    project = 0
    sprint = 0
    department = ""
    typename = ""
    statusname = ""
    priorityname = ""
    

    def json_to_task(self, json):
        if json is None:
            return False
        
        task_attributes = [
            ("task_id", str),
            ("task_subject", str),
            ("task_tender_price", float),
            ("task_estimatedtime", int),
            ("task_start_datetime", str),
            ("task_end_datetime", str),
            ("tasks_createdate", str),
            ("task_deadline", str),
            ("task_scrum_value", int),
            ("task_scrum_effort", int),
            ("employee", lambda x: x["fullname"] if "fullname" in x else None),
            ("project", lambda x: x["project_name"] if "project_name" in x else None),
            ("reference", lambda x: x["ref_name"] if "ref_name" in x else None),
            ("type", lambda x: x["type_name"] if "type_name" in x else None),
            ("status", lambda x: x["status_name"] if "status_name" in x else None),
            ("priority", lambda x: x["priority_name"] if "priority_name" in x else None),
            ("sprint", lambda x: x["sprint_name"] if "sprint_name" in x else None)
        ]
        
        for attribute_name, type_converter in task_attributes:
            try:
                attribute_value = json.get(attribute_name)
                if attribute_value is not None:
                    setattr(self, attribute_name, type_converter(attribute_value))
                else:
                    setattr(self, attribute_name, None)
            except (ValueError, TypeError):
                setattr(self, attribute_name, None)
    
    def addEventJson(self, eventjson):
        print(eventjson)
        for eventitem in eventjson:
            event = Event(self.context)
            event.json_to_event(eventitem)
            print(event)
            self.events.append(event)
            print(self.events)
    
    def __str__(self):
        string = f"Task ID: {self.task_id} Task Subject: {self.task_subject} \n"
        number_of_events = len(self.events)
        string += f"number of events: {number_of_events}"
        #for event in self.events:
        #   string += f"{event} \n"
        
        string += "------------------------------------ \n"

        return string