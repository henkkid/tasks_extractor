from Model.Sprint import Sprint

class SprintList:

    data = []
    def __init__(self, ApiControler):
        self.ApiControl = ApiControler
        self.create_sprintList()
        

    def addSprint(self, sprint):
        if(sprint.isWeekSprint()):
            self.data.append(sprint)
    
    def create_sprintList(self):
        data = self.ApiControl.getSprintDatafromApi()
        self.extract_sprintData(data)
        

    def extract_sprintData(self, data):
        for item in data:
            data = Sprint(item)
            self.addSprint(data)
    
    def get_Sprint_by_Date(self, date):
        for item in self.data:
            if item.date_in_sprint(date):
                return item
        return None
    
    def __str__(self):
        return ' \n'.join(str(item) for item in self.data)