import os
import xlsxwriter
from dateutil import parser

class ExcelControler:

    tasklist = []
    eventlist = []

    def __init__(self, tasklist):
        self.tasklist = tasklist

    def create_excel(self, location, name):
        location = self.set_absolute_location(location)
        self.check_folder_exsist_or_create(location)
        self.extract_events_from_tasks()
        self.create_workbook(location, name)
        self.create_event_worksheet()
        self.create_task_worksheet()
        self.workbook.close()
        
    def set_absolute_location(self, location):
        current_path = os.getcwd()
        location = current_path + location
        return location

    def check_folder_exsist_or_create(self, location):
            if os.path.isdir(location):
                return True
            else:
                os.mkdir(location)
                return True  
        

    def extract_events_from_tasks(self):
        for task in self.tasklist:
            for event in task.events:
                self.eventlist.append(event)

    def create_workbook(self, location, name):
        path = location + name
        self.workbook = xlsxwriter.Workbook(path)
        self.workbook.remove_timezone = True
    
    def create_worksheet(self, name):
        return self.workbook.add_worksheet(name)
    
    def create_event_worksheet(self):
        worksheet = self.create_worksheet('geboekte uren')

        worksheet.write(0, 0, 'task_id')
        worksheet.write(0, 1, 'event_id')
        worksheet.write(0, 2, 'event_name')
        worksheet.write(0, 3, 'event_start_date')
        worksheet.write(0, 4, 'event_end_date')
        worksheet.write(0, 5, 'time_in_minutes')
        

        for row_num, event in enumerate(self.eventlist):
            row_num += 1
            worksheet.write(row_num, 0, event.task_id)
            worksheet.write(row_num, 1, event.event_id)
            worksheet.write(row_num, 2, event.event_name)
            worksheet.write_datetime(row_num, 3, event.event_start_date)
            worksheet.write_datetime(row_num, 4, event.event_end_date)
            worksheet.write(row_num, 5, event.time_in_minutes)
            

        worksheet.autofit()
  
    def create_task_worksheet(self):
        worksheet = self.create_worksheet('tasks')

        worksheet.write(0, 0, 'task_id')
        worksheet.write(0, 1, 'task_subject')
        worksheet.write(0, 2, 'task_tender_price')
        worksheet.write(0, 3, 'task_estimatedtime')
        worksheet.write(0, 4, 'task_start_datetime')
        worksheet.write(0, 5, 'task_end_datetime')
        worksheet.write(0, 6, 'task_createdate')
        worksheet.write(0, 7, 'task_deadline')
        worksheet.write(0, 8, 'task_scrum_value')
        worksheet.write(0, 9, 'task_scrum_effort')
        worksheet.write(0, 10, 'employee')
        worksheet.write(0, 11, 'project')
        worksheet.write(0, 12, 'sprint')
        worksheet.write(0, 13, 'department')
        worksheet.write(0, 14, 'typename')
        worksheet.write(0, 15, 'statusname')
        worksheet.write(0, 16, 'priorityname')
        worksheet.write(0, 17, 'total_time_of_events_in_minutes')
        worksheet.write(0, 18, 'total_time_of_events_in_hours')


        for row_num, task in enumerate(self.tasklist):
            row_num += 1
            worksheet.write(row_num, 0, task.task_id)
            worksheet.write(row_num, 1, task.task_subject)
            worksheet.write(row_num, 2, task.task_tender_price)
            worksheet.write(row_num, 3, task.task_estimatedtime)
            worksheet.write_datetime(row_num, 4, parser.parse(task.task_start_datetime))
            worksheet.write_datetime(row_num, 5, parser.parse(task.task_end_datetime))
            worksheet.write_datetime(row_num, 6, parser.parse(task.tasks_createdate))
            try:
                worksheet.write_datetime(row_num, 7, parser.parse(task.task_deadline))
            except:
                worksheet.write(row_num, 7, "" )
            worksheet.write(row_num, 8, task.task_scrum_value)
            worksheet.write(row_num, 9, task.task_scrum_effort)
            worksheet.write(row_num, 10, task.employee)
            worksheet.write(row_num, 11, task.project)
            worksheet.write(row_num, 12, task.sprint)
            worksheet.write(row_num, 13, task.reference)
            worksheet.write(row_num, 14, task.type)
            worksheet.write(row_num, 15, task.status)
            worksheet.write(row_num, 16, task.priority)
            worksheet.write(row_num, 17, task.total_time_of_events_in_minutes)
            worksheet.write(row_num, 18, task.total_time_of_events_in_hours)

        worksheet.autofit()

