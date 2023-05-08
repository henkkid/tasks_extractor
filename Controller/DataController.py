from tkinter.messagebox import showinfo
import json

import pandas as pd

from Controller.Api import ApiControler
from Controller.DataControllerHelper import DataControllerHelper
from Model.Task import Task

class DataControler:
    
    #dict with the names of the month as key and the month number as value
    months = {
        'January' : 1,
        'February' : 2,
        'March' : 3,
        'April' : 4,
        'May' : 5,
        'June' : 6,
        'July' : 7,
        'August' : 8,
        'September' : 9,
        'October' : 10,
        'November' : 11,
        'December' : 12
    }

    departments = {
        "Backend" : 445,
        "Frontend" : 447
    }

    input_data = {
        'month' : '',
        'monthNumber' : 0,
        'department' : '',
        'departmentNumber' : 0,
        'width' : 0	
    }

    def __init__(self, Context):
        self.AppContext = Context
        self.Api = Context.getApiController()
        self.Helper = DataControllerHelper()

    def setMonth(self, month):
        self.input_data['month'] = month
        try: 
            self.input_data['monthNumber'] = self.months[month]
        except:
            showinfo("Error", "Invalid month")

    def setDepartment(self, department):
        self.input_data['department'] = department
        try: 
            self.input_data['departmentNumber'] = self.departments[department]
        except:
            showinfo("Error", "Invalid department")

    def setAnalysesWidth(self, width):
        try:
            if int(width) <=0:
                showinfo("Error", "analyeses width is incorrect")
            else:
                self.input_data['width'] = int(width)
        except:
            showinfo("Error", "analyeses width is incorrect")
                       
    

    def generateExcel(self):
        if self.input_data['monthNumber'] == 0 or self.input_data['departmentNumber'] == 0 or self.input_data['width'] <= 0:
            return False
        else:
            self.getData()
            return True
        

    def getData(self):
        sprints = self.getSprints(self.input_data['monthNumber'],  self.input_data['width'])
        tasks = self.getTasks(sprints)
        #for task in tasks:
            #print(task)
        
        
        
    
    def getTasks(self, sprints):
        tasks = []

        for key in sprints:
            data = self.Api.getTasksBySprintId(sprints[key], self.input_data['departmentNumber'])
            for item in data:
                task = Task(self.AppContext)
                task.json_to_task(item)
                if len(item['events']) > 0:
                    task.addEventJson(item['events'])
                tasks.append(task)
        
        return tasks

    def getSprints(self, monthnumber, analyses_width):
        data = self.Api.getSprintDatafromApi()

        df = pd.DataFrame(data)
        df = df[df['sprint_name'].str.contains("Week") == True]
        df['sprint_start_date'] = pd.to_datetime(df['sprint_start_date']).dt.month
        df['sprint_end_date'] = pd.to_datetime(df['sprint_end_date']).dt.month

        outputdf = self.trim_dataframe(monthnumber, analyses_width, df)
        outputdf = outputdf.drop(['sprint_start_date', 'sprint_end_date'], axis=1)
        outputDict = outputdf.set_index('sprint_name')['sprint_id'].to_dict()

        return outputDict

    def trim_dataframe(self, monthnumber, analyses_width, df):
        outputdf = pd.DataFrame()

        i = self.Helper.substract_wrapping(monthnumber, analyses_width)
        while True:
            subdf = df[df['sprint_end_date'] == i]
            subdf = subdf.sort_values(by=['sprint_start_date'])
            subdf = subdf.reset_index(drop=True)
            
            outputdf = pd.concat([outputdf, subdf])
            i = self.Helper.add_wrapping(i, 1)

            if self.Helper.add_wrapping(monthnumber, analyses_width + 1) == i:
                break

        outputdf = outputdf.reset_index(drop=True)
        return outputdf
    
    
    
    