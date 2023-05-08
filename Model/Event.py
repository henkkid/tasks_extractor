from datetime import datetime

class Event:

    event_id = None
    event_start_date = None
    event_end_date = None
    event_name = None
    time_in_minutes = None
    sprint = None


    def __init__(self, context):
        self.sprintlist = context.SprintList
        
    
    def json_to_event(self, json):
        
        if json is None:
            return False
        else:
            event_atributes =[
                ('event_id', int),
                ('event_start_date', str),
                ('event_end_date', str),
                ('event_name', str)
            ]
        
            for attribute_name, type_converter in event_atributes:
                try:
                    attribute_value = json.get(attribute_name)
                    if attribute_value is not None:
                        setattr(self, attribute_name, type_converter(attribute_value))
                    else:
                        setattr(self, attribute_name, None)
                except(ValueError, TypeError):
                    setattr(self, attribute_name, None)
            
            self.format_data()
            self.get_sprint()
            self.calculate_time_in_minutes()
            
        return True
    
    def calculate_time_in_minutes(self):
        self.time_in_minutes = (self.event_end_date - self.event_start_date).total_seconds() / 60
        return self.time_in_minutes

    def format_data(self):
        if(type(self.event_start_date) is str):
            self.event_start_date = datetime.fromisoformat(self.event_start_date)
        if(type(self.event_end_date) is str):
            self.event_end_date = datetime.fromisoformat(self.event_end_date)

    def get_sprint(self):
        self.sprint = self.sprintlist.get_Sprint_by_Date(self.event_end_date)
        

    def __str__(self):
        return f'Event: {self.event_name} - {self.event_start_date} - {self.event_end_date} - {self.time_in_minutes} - {self.sprint}'