from Controller.Api import ApiControler
from Controller.ApiAuthentication import ApiAuthentication
from Model.SprintList import SprintList


class AppContext:

    SprintList = None
    ApiControl = None

    def __init__(self):
        self.create_ApiContoller()
        self.SprintList = SprintList(self.ApiControl)

    def create_ApiContoller(self):
        Auth = ApiAuthentication()
        self.ApiControl = ApiControler(Auth)
    
    def getApiController(self):
        return self.ApiControl

    def getSprintList(self):
        return self.SprintList