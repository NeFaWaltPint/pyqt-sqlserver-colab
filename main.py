# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QApplication, QMainWindow
from controllers.create_drop_db import checkCreateDropDB
from controllers.database import SessionLocal, config
from controllers.forms.turno import logic_Turno
from controllers.forms.venta import logic_Venta
from views.main_ui import Ui_MainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect buttons
        self.ui.PB_Login.clicked.connect(self.login)

        self.views = []


    def login(self):
        user = self.ui.LE_User.text()
        password = self.ui.LE_Pass.text()
        self.ui.LE_User.setText("")
        self.ui.LE_Pass.setText("")

        if user == config['USERS']['admin'] and password == config['PASSWORDS']['admin']:
            session = SessionLocal()
            try:

                self.views.append(logic_Turno(session))
                self.ui.Tab_Views.addTab(self.views[-1].getView(), "Turno")
                self.views.append(logic_Venta(session))
                self.ui.Tab_Views.addTab(self.views[-1].getView(), "Venta")

                self.ui.Tab_Views.setCurrentIndex(1)
                self.ui.Tab_Views.setTabEnabled(0, False)
            
            except Exception as e:
                print(f"Ups! Error: {e}")
            finally:
                session.close()
            return
        
        if user == config['USERS']['empleado'] and password == config['PASSWORDS']['empleado']:
            session = SessionLocal()
            try:

                self.views.append(logic_Venta(session))
                self.ui.Tab_Views.addTab(self.views[-1].getView(), "Venta")
                self.ui.Tab_Views.setCurrentIndex(1)
                self.ui.Tab_Views.setTabEnabled(0, False)
            
            except Exception as e:
                print(f"Ups! Error: {e}")
            finally:
                session.close()
            return    
        

if __name__ == '__main__':
    checkCreateDropDB()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
