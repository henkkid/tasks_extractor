from datetime import datetime

class Sprint:

    sprint_id = 0
    sprint_name = ""
    sprint_start_date = None
    sprint_end_date = None

    def __init__(self, sprint_id, sprint_name, sprint_start_date, sprint_end_date):
        self.sprint_id = sprint_id
        self.sprint_name = sprint_name
        self.sprint_start_date = sprint_start_date
        self.sprint_end_date = sprint_end_date
        
    def __init__(self, data):
        self.convert_data_to_sprint(data)
        self.format_data()

    def format_data(self):
        if(type(self.sprint_start_date) == str):
            self.sprint_start_date = datetime.fromisoformat(self.sprint_start_date)
        if(type(self.sprint_end_date) == str):
            self.sprint_end_date = datetime.fromisoformat(self.sprint_end_date)
        if "Week" in self.sprint_name:
            self.Week_Sprint = True
        else:
            self.Week_Sprint = False

    def convert_data_to_sprint(self, data):
        sprint_attributes =[
            ("sprint_id", str),
            ("sprint_name", str),
            ("sprint_start_date", str),
            ("sprint_end_date", str)  
        ]
        
        for attribute_name, type_converter in sprint_attributes:
            try:
                attribute_value = data.get(attribute_name)
                if attribute_value is not None:
                    setattr(self, attribute_name, type_converter(attribute_value))
                else:
                    setattr(self, attribute_name, None)
            except (ValueError, TypeError):
                setattr(self, attribute_name, None)
    
    def get_sprint_id(self):
        return self.sprint_id
    
    def get_sprint_name(self):
        return self.sprint_name
    
    def get_sprint_start_date(self):
        return self.sprint_start_date
    
    def get_sprint_end_date(self):
        return self.sprint_end_date

    def date_in_sprint(self, date):
        return self.sprint_start_date <= date <= self.sprint_end_date
    
    def isWeekSprint(self):
        return self.Week_Sprint
    
    def __str__(self):
        return f"Sprint: {self.sprint_name}"