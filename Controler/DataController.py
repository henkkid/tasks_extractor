
from tkinter.messagebox import showinfo
import json

import pandas as pd

from Controler.Api import ApiControler
from Controler.DataControllerHelper import DataControllerHelper
from Controler.ExcelControler import ExcelControler
from Model.Task import Task
from Model.Event import Event

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
        if self.input_data['monthNumber'] == 0 or self.input_data['departmentNumber'] == 0:
            return False
        else:
            tasks = self.getTasks()
            Excelcon = ExcelControler(tasks)
            Excelcon.create_excel("\exports", "\export.xlsx")
            return True
    
    def getTasks(self):
        tasks = []

        
        data = self.Api.getTaskswithCreateDateAfter("2023-01-01", self.input_data['departmentNumber'])
        for item in data:
            task = self.createTaskFromJson(item)
            print(task)
            
            if len(item['events']) > 0:
                for event in item['events']:
                    event = self.createEventFromJson(event)
                    event.task_id = task.task_id
                    event.compute_other_values()
                    task.addEvent(event)
            task.calculateTotalTimeOfEvents()
            tasks.append(task)
                
        return tasks
    
    def createEventFromJson(self, json):
        event =  Event(self.AppContext)

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
                        setattr(event, attribute_name, type_converter(attribute_value))
                    else:
                        setattr(event, attribute_name, None)
                except(ValueError, TypeError):
                    setattr(event, attribute_name, None)

        return event

    def createTaskFromJson(self, json):
        if json is None:
            return False
        
        extracted_data = Task(self.AppContext)
        
        
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
                    setattr(extracted_data, attribute_name, type_converter(attribute_value))
                else:
                    setattr(extracted_data, attribute_name, None)
            except (ValueError, TypeError):
                setattr(extracted_data, attribute_name, None)
        return extracted_data

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
    
    
    
    