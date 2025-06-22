# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from views.forms.DetalleCompra_ui import Ui_F_Compra
from models.models import Compra, Proveedor, Producto, DetalleCompra

class logic_DetalleCompra(object):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Compra()
        self.view.setupUi(self.widget)

        self.linkActions()
        self.buildTable()
        self.populateTable1()
        
    def getView(self):
        return self.widget

    def linkActions(self):
        self.view.actualizar.clicked.connect(self.populateTable1)
        self.view.tableWidget_1.cellClicked.connect(self.populateTable2)

    def buildTable(self):
        self.columnas_compras = ["Id", "Proveedor", "Total Compra", "Fecha"]
        self.view.tableWidget_1.setColumnCount(len(self.columnas_compras))
        self.view.tableWidget_1.setHorizontalHeaderLabels(self.columnas_compras)

        self.columnas_detalles = ["Producto", "Cantidad", "Precio Unitario", "Subtotal"]
        self.view.tableWidget_2.setColumnCount(len(self.columnas_detalles))
        self.view.tableWidget_2.setHorizontalHeaderLabels(self.columnas_detalles)

    def populateTable1(self):
        self.registros_1 = self.db.query(Compra).all()
        self.view.tableWidget_1.setRowCount(len(self.registros_1))

        for fila_idx, objeto in enumerate(self.registros_1):
            self.view.tableWidget_1.setItem(fila_idx, 0, QTableWidgetItem(str(objeto.id_compra)))
            proveedor = self.db.query(Proveedor).get(objeto.id_proveedor)
            self.view.tableWidget_1.setItem(fila_idx, 1, QTableWidgetItem(str(proveedor.nombre)))
            self.view.tableWidget_1.setItem(fila_idx, 2, QTableWidgetItem(str(objeto.total_compra)))
            self.view.tableWidget_1.setItem(fila_idx, 3, QTableWidgetItem(str(objeto.fecha)))
    
    def populateTable2(self, row, _):
        if row >= 0 and row < len(self.registros_1):
            compra = self.registros_1[row]
            detalles = self.db.query(DetalleCompra).filter(DetalleCompra.id_compra == compra.id_compra).all()
            self.view.tableWidget_2.setRowCount(len(detalles))

            for fila_idx, detalle in enumerate(detalles):
                producto = self.db.query(Producto).get(detalle.id_producto)
                self.view.tableWidget_2.setItem(fila_idx, 0, QTableWidgetItem(str(producto.nombre)))
                self.view.tableWidget_2.setItem(fila_idx, 1, QTableWidgetItem(str(detalle.cantidad)))
                self.view.tableWidget_2.setItem(fila_idx, 2, QTableWidgetItem(str(detalle.precio_unitario)))
                self.view.tableWidget_2.setItem(fila_idx, 3, QTableWidgetItem(str(detalle.cantidad * detalle.precio_unitario)))

    def save(self):
        print("Guardar")

    def clear(self):
        
        print("Limpiar")