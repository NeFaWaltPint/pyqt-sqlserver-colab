# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QApplication, QMainWindow
from controllers.create_drop_db import checkCreateDropDB
from controllers.database import SessionLocal, config
from controllers.forms.Proveedor import logic_Proveedor
from controllers.forms.compra import logic_Compra
from controllers.forms.detallecompra import logic_DetalleCompra
from controllers.forms.detalleventa import logic_DetalleVenta
from controllers.forms.empleado import logic_Empleado
from controllers.forms.horarioempleado import logic_HorarioEmpleado
from controllers.forms.juego import logic_Juego
from controllers.forms.mesabillar import logic_MesaBillar
from controllers.forms.metodopago import logic_MetodoPago
from controllers.forms.producto import logic_Producto
from controllers.forms.turno import logic_Turno
from controllers.forms.venta import logic_Venta
from models.models import Empleado
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
                self.viewsWlogic.append(logic_Empleado(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Empleado")
                self.viewsWlogic.append(logic_HorarioEmpleado(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Horario Empleado")
                self.viewsWlogic.append(logic_MetodoPago(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Método de Pago")
                self.viewsWlogic.append(logic_Venta(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Venta")
                self.viewsWlogic.append(logic_DetalleVenta(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Detalle Venta")
                self.viewsWlogic.append(logic_Proveedor(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Proveedor")
                self.viewsWlogic.append(logic_Producto(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Producto")
                self.viewsWlogic.append(logic_Compra(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Realizar Compra")
                self.viewsWlogic.append(logic_DetalleCompra(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Detalle Compra")
                self.viewsWlogic.append(logic_Juego(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Juego")
                self.viewsWlogic.append(logic_MesaBillar(sessionDB))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Mesa Billar")

                self.ui.Tab_Views.setCurrentIndex(1)
                self.ui.Tab_Views.setTabEnabled(0, False)
            
            except Exception as e:
                print(f"Ups! Error: {e}")
            finally:
                sessionDB.close()
            return
        
        empleado = SessionLocal().query(Empleado).filter(Empleado.nombre == user).first()
        if empleado and password == config['PASSWORDS']['empleado']:
            sessionDB = SessionLocal()
            try:

                self.viewsWlogic.append(logic_Venta(sessionDB, empleado))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Venta")
                self.viewsWlogic.append(logic_DetalleVenta(sessionDB, empleado))
                self.ui.Tab_Views.addTab(self.viewsWlogic[-1].getView(), "Detalle Venta")

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
