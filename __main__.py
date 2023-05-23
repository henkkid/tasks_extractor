from Controler.ApiAuthentication import ApiAuthentication
from Controler.DataController import DataControler
from View.gui import gui
from Model.AppContext import AppContext



def Main():
    context = AppContext()
    Gui = gui(DataControler(context))

if __name__ == "__main__":
    Main()




