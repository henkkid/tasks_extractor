import tkinter as tk
from tkinter import ttk
from calendar import month_name
from tkinter.messagebox import showinfo

class gui:
    
    def __init__(self, DataControler):
        self.root = tk.Tk()
        self.DataController = DataControler
        
        self.setWindowSettings()
        self.fillGui()
        self.root.mainloop()


    def setWindowSettings(self):
        self.root.geometry("500x250")
        self.root.title("Data Extractor")
        self.root.configure(background="black")
        self.root.resizable(False, False)
    

    def fillGui(self):
        label = tk.Label(self.root, text="Please select a month", font=("Arial"), bg="black", fg="white")
        label.pack(fill=tk.X,padx=5, pady=5)

        selected_month = tk.StringVar()
        month_cb = ttk.Combobox(self.root, textvariable=selected_month)
        month_cb["values"] = [month_name[i] for i in range(1,13)]
        month_cb.current(1)
        month_cb['state'] = 'readonly'

        month_cb.pack(fill=tk.X,padx=5, pady=5)

        label = tk.Label(self.root, text="Please select a analyses width in months", font=("Arial"), bg="black", fg="white")
        label.pack(fill=tk.X,padx=5, pady=5)

        selected_analyses_width = tk.StringVar()
        analyses_width_cb = ttk.Combobox(self.root, textvariable=selected_analyses_width)
        analyses_width_cb["values"] = [1,2,3,4]
        analyses_width_cb.current(0)
        analyses_width_cb['state'] = 'readonly'

        analyses_width_cb.pack(fill=tk.X,padx=5, pady=5)

        label = tk.Label(self.root, text="Please select a department", font=("Arial"), bg="black", fg="white")
        label.pack(fill=tk.X,padx=5, pady=5)

        selected_department = tk.StringVar()
        department_cb = ttk.Combobox(self.root, textvariable=selected_department)
        department_cb["values"] = ["Backend", "Frontend"]
        department_cb.current(0)
        department_cb['state'] = 'readonly'

        department_cb.pack(fill=tk.X,padx=5, pady=5)

        

        department_cb.pack(fill=tk.X,padx=5, pady=5)

        button = tk.Button(self.root, text="Generate Excel", command=lambda: self.extractData(selected_month.get(), selected_department.get(), selected_analyses_width.get()))
        button.pack(fill=tk.X,padx=5, pady=5)

    def extractData(self, month, department, analyes_width):
        self.DataController.setMonth(month)
        self.DataController.setDepartment(department)
        self.DataController.setAnalysesWidth(analyes_width)
        
        if self.DataController.generateExcel():
            showinfo(
                title="Success",
                message=f'Data was extracted successfully'
            )
        else:
            showinfo(
                title="Error",
                message=f'Data was not extracted successfully'
            )
        
