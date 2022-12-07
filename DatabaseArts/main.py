from SQLiteDataBaseClass import SQLiteDataBase
from InterfaceClass import Interface
from AppControllerClass import AppController


class MainApp:

    def __init__(self):
        self.database = SQLiteDataBase()
        self.controller = AppController(self.database)
        self.interface = Interface(self.controller)

    def run(self):
        self.controller.start()
        self.interface.run()


if __name__ == '__main__':
    app = MainApp()
    app.run()
