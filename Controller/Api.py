import requests


class ApiControler:

    def __init__(self, Auth):
        self.Auth = Auth
        self.DefaultHeaders = { "Authorization": self.Auth.getToken() }

    def getSprintDatafromApi(self):
        requestUrl = self.Auth.getAPIBaseUrl() + '/sprints'
        response = requests.get(requestUrl,  headers=self.DefaultHeaders)
        
        data = response.json()['data']
        return data

    def getTasksBySprintId(self, sprintId, departmentId):
        requestUrl = self.Auth.getAPIBaseUrl() + '/tasks?filter[reference_id]='+ str(departmentId) +'&filter[task_sprint]='+ str(sprintId) + '&include=employee,project,reference,type,status,priority,sprint,events'
        response = requests.get(requestUrl,  headers=self.DefaultHeaders)

        data = response.json()['data']
        meta = response.json()['meta']

        if meta['last_page'] > 1:
            lastPage = meta['last_page']

            i = 2
            while i <= lastPage:
                requestUrl = self.Auth.getAPIBaseUrl() + '/tasks?filter[reference_id]='+ str(departmentId) +'&filter[task_sprint]='+ str(sprintId) + '&include=employee,project,reference,type,status,priority,sprint,events&page='+ str(i)
                response = requests.get(requestUrl,  headers=self.DefaultHeaders)
                data.extend(response.json()['data'])
        

        
        return data

    