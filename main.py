# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QApplication, QMainWindow
from controllers.create_drop_db import checkCreateDropDB
from controllers.database import SessionLocal, config
from controllers.forms.Proveedor import logic_Proveedor
from controllers.forms.empleado import logic_Empleado
from controllers.forms.metodopago import logic_MetodoPago
from controllers.forms.producto import logic_Producto
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

        self.viewsWlogic = []


    def login(self):
        user = self.ui.LE_User.text()
        password = self.ui.LE_Pass.text()
        self.ui.LE_User.setText("")
        self.ui.LE_Pass.setText("")

        if user == config['USERS']['admin'] and password == config['PASSWORDS']['admin']:
            sessionDB = SessionLocal()
            try:

                self.viewsWlogic.append(logic_Turno(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Turno")
                self.viewsWlogic.append(logic_MetodoPago(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Método de Pago")
                self.viewsWlogic.append(logic_Empleado(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Empleado")
                self.viewsWlogic.append(logic_Venta(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Venta")
                self.viewsWlogic.append(logic_Proveedor(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Proveedor")
                self.viewsWlogic.append(logic_Producto(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Producto")

                self.ui.Tab_Views.setCurrentIndex(1)
                self.ui.Tab_Views.setTabEnabled(0, False)
            
            except Exception as e:
                print(f"Ups! Error: {e}")
            finally:
                sessionDB.close()
            return
        
        if user == config['USERS']['empleado'] and password == config['PASSWORDS']['empleado']:
            sessionDB = SessionLocal()
            try:

                self.viewsWlogic.append(logic_Venta(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Venta")
                self.ui.Tab_Views.setCurrentIndex(1)
                self.ui.Tab_Views.setTabEnabled(0, False)
            
            except Exception as e:
                print(f"Ups! Error: {e}")
            finally:
                sessionDB.close()
            return    
        

if __name__ == '__main__':
    checkCreateDropDB()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
