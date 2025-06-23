# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from views.forms.Compra_ui import Ui_F_Compra
from models.models import Compra, Proveedor, Producto, DetalleCompra

class logic_Compra(object):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Compra()
        self.view.setupUi(self.widget)

        self.linkActions()
        self.loadSelects()
        self.buildTable()
        
    def getView(self):
        return self.widget

    def linkActions(self):
        self.view.agregar.clicked.connect(self.carrito)
        self.view.quitar.clicked.connect(self.remove)
        self.view.realizar_compra.clicked.connect(self.save)
    
    def loadSelects(self):
        self.proveedores = self.db.query(Proveedor).all()
        self.view.proveedor.addItem("Seleccione un proveedor", userData=None)
        for proveedor in self.proveedores:
            self.view.proveedor.addItem(str(proveedor.nombre), userData=proveedor.id_proveedor)
        self.productos = self.db.query(Producto).all()
        self.view.producto.addItem("Seleccione un producto", userData=None)
        for producto in self.productos:
            self.view.producto.addItem(str(producto.nombre), userData=producto.id_producto)

    def buildTable(self):
        self.columnas = ["Producto", "Cantidad", "Precio", "Subtotal"]
        self.view.tableWidget.setColumnCount(len(self.columnas))
        self.view.tableWidget.setHorizontalHeaderLabels(self.columnas)

    def carrito(self):
        fila = self.view.tableWidget.rowCount()
        self.view.tableWidget.insertRow(fila)
        producto_id = self.view.producto.currentData()
        cantidad = self.view.cantidad.value()
        
        producto = next((p for p in self.productos if p.id_producto == producto_id), None)
        precio = producto.precio_venta
        subtotal = cantidad * precio

        itemProducto = QTableWidgetItem(producto.nombre)
        itemProducto.setData(Qt.ItemDataRole.UserRole, producto.id_producto)
        self.view.tableWidget.setItem(fila, 0, itemProducto)
        self.view.tableWidget.setItem(fila, 1, QTableWidgetItem(str(cantidad)))
        self.view.tableWidget.setItem(fila, 2, QTableWidgetItem(str(precio)))
        self.view.tableWidget.setItem(fila, 3, QTableWidgetItem(str(subtotal)))

        self.calcTotal()

    def remove(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0:
            self.view.tableWidget.removeRow(actual_row)
        self.calcTotal()
    
    def save(self):
        detalles = []
        total = 0
        for row in range(self.view.tableWidget.rowCount()):
            producto_id = self.view.tableWidget.item(row, 0).data(Qt.ItemDataRole.UserRole)
            cantidad = int(self.view.tableWidget.item(row, 1).text())
            precio = float(self.view.tableWidget.item(row, 2).text())
            subtotal = float(self.view.tableWidget.item(row, 3).text())
            detalles.append(
                DetalleCompra(
                    id_compra=None,
                    id_producto=producto_id,
                    cantidad=cantidad,
                    precio_unitario=precio,
                )
            )
            total += subtotal
        
        compra = Compra(
            id_proveedor=self.view.proveedor.currentData(),
            total_compra=total,
            fecha=datetime.combine(datetime.today().date(), datetime.min.time())
        )
        self.db.add(compra)
        self.db.commit()
        compra_id = compra.id_compra

        for detalle in detalles:
            detalle.id_compra = compra_id
            self.db.add(detalle)

        for detalle in detalles:
            producto = self.db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
            if producto:
                producto.cantidad_stock += detalle.cantidad

        self.db.commit()

        self.clear()

    def clear(self):
        self.view.proveedor.setCurrentIndex(0)
        self.view.producto.setCurrentIndex(0)
        self.view.cantidad.setValue(0)
        self.view.tableWidget.setRowCount(0)
        self.view.L_total.setText("$ 0.00")
    
    def calcTotal(self):
        total = 0
        for row in range(self.view.tableWidget.rowCount()):
            subtotal = float(self.view.tableWidget.item(row, 3).text())
            total += subtotal
        self.view.L_total.setText("$ " + str(total))