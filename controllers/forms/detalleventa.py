# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from views.forms.DetalleVenta_ui import Ui_F_Venta
from models.models import Venta, Empleado, Producto, MetodoPago, DetalleVenta, MesaBillar

class logic_DetalleVenta(object):
    def __init__(self, db: Session, userIn: Empleado = None):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Venta()
        self.view.setupUi(self.widget)
        self.user = userIn

        self.linkActions()
        self.buildTable()
        self.populateTable1()
        
    def getView(self):
        return self.widget

    def linkActions(self):
        self.view.actualizar.clicked.connect(self.populateTable1)
        self.view.tableWidget_1.cellClicked.connect(self.populateTable2)

    def buildTable(self):
        self.columnas_ventas = ["Id", "Empleado", "Total Venta", "Metodo de Pago", "Mesa", "Fecha"]
        self.view.tableWidget_1.setColumnCount(len(self.columnas_ventas))
        self.view.tableWidget_1.setHorizontalHeaderLabels(self.columnas_ventas)

        self.columnas_detalles = ["Producto", "Cantidad", "Precio Unitario", "Subtotal"]
        self.view.tableWidget_2.setColumnCount(len(self.columnas_detalles))
        self.view.tableWidget_2.setHorizontalHeaderLabels(self.columnas_detalles)

    def populateTable1(self):
        self.registros_1 = []
        if self.user != None:
            self.registros_1 = self.db.query(Venta).filter(Venta.id_empleado == self.user.id_empleado).all()
        else:
            self.registros_1 = self.db.query(Venta).all()
        self.view.tableWidget_1.setRowCount(len(self.registros_1))

        for fila_idx, objeto in enumerate(self.registros_1):
            self.view.tableWidget_1.setItem(fila_idx, 0, QTableWidgetItem(str(objeto.id_venta)))
            if self.user != None:
                self.view.tableWidget_1.setItem(fila_idx, 1, QTableWidgetItem(str(self.user.nombre) + " " + str(self.user.apellido)))
            else:
                empleado = self.db.query(Empleado).get(objeto.id_empleado) if objeto.id_empleado else None
                if empleado != None:
                    self.view.tableWidget_1.setItem(fila_idx, 1, QTableWidgetItem(str(empleado.nombre) + " " + str(empleado.apellido)))
                else:
                    self.view.tableWidget_1.setItem(fila_idx, 1, QTableWidgetItem(str("Admin")))
            self.view.tableWidget_1.setItem(fila_idx, 2, QTableWidgetItem(str(objeto.total_venta)))
            metodo_pago = self.db.query(MetodoPago).get(objeto.id_metodo_pago) if objeto.id_metodo_pago else None
            if metodo_pago != None:
                self.view.tableWidget_1.setItem(fila_idx, 3, QTableWidgetItem(str(metodo_pago.descripcion)))
            else:
                self.view.tableWidget_1.setItem(fila_idx, 3, QTableWidgetItem(str("-")))
            if objeto.id_mesa != None:
                self.view.tableWidget_1.setItem(fila_idx, 4, QTableWidgetItem(str(objeto.id_mesa)))
            else:
                self.view.tableWidget_1.setItem(fila_idx, 4, QTableWidgetItem(str("Sin mesa")))
            self.view.tableWidget_1.setItem(fila_idx, 5, QTableWidgetItem(str(objeto.fecha)))

    def populateTable2(self, row, _):
        if row >= 0 and row < len(self.registros_1):
            venta = self.registros_1[row]
            detalles = self.db.query(DetalleVenta).filter(DetalleVenta.id_venta == venta.id_venta).all()
            self.view.tableWidget_2.setRowCount(len(detalles))

            for fila_idx, detalle in enumerate(detalles):
                producto = self.db.query(Producto).get(detalle.id_producto)
                self.view.tableWidget_2.setItem(fila_idx, 0, QTableWidgetItem(str(producto.nombre)))
                self.view.tableWidget_2.setItem(fila_idx, 1, QTableWidgetItem(str(detalle.cantidad)))
                self.view.tableWidget_2.setItem(fila_idx, 2, QTableWidgetItem(str(detalle.precio_unitario)))
                self.view.tableWidget_2.setItem(fila_idx, 3, QTableWidgetItem(str(detalle.cantidad * detalle.precio_unitario)))
