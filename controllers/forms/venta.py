# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from views.forms.Venta_ui import Ui_F_Venta
from models.models import Venta, Empleado, Producto, MetodoPago, DetalleVenta, MesaBillar

class logic_Venta(object):
    def __init__(self, db: Session, userIn: Empleado = None):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Venta()
        self.view.setupUi(self.widget)
        self.user = userIn

        if self.user != None:
            self.view.L_Empleado.setText(self.user.nombre + " " + self.user.apellido)

        self.linkActions()
        self.loadSelects()
        self.buildTable()
        
    def getView(self):
        return self.widget

    def linkActions(self):
        self.view.agregar.clicked.connect(self.carrito)
        self.view.quitar.clicked.connect(self.remove)
        self.view.realizar_venta.clicked.connect(self.save)
    
    def loadSelects(self):
        self.mesas = self.db.query(MesaBillar).all()
        self.view.mesa.clear()
        self.view.mesa.addItem("Seleccione una mesa si se requiere", userData=None)
        for mesa in self.mesas:
            self.view.mesa.addItem(str(mesa.id_mesa), userData=mesa.id_mesa)

        self.productos = self.db.query(Producto).filter(Producto.cantidad_stock >= 1).all()
        self.view.producto.clear()
        self.view.producto.addItem("Seleccione un producto", userData=None)
        for producto in self.productos:
            self.view.producto.addItem(str(producto.nombre) + " (" + str(producto.cantidad_stock) + ")", userData=producto.id_producto)

        self.metodopago = self.db.query(MetodoPago).all()
        self.view.metodo_pago.clear()
        self.view.metodo_pago.addItem("Seleccione un metodo de pago", userData=None)
        for metodo in self.metodopago:
            self.view.metodo_pago.addItem(str(metodo.descripcion), userData=metodo.id_metodo_pago)

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
        
        if cantidad > producto.cantidad_stock:
            self.view.cantidad.setValue(producto.cantidad_stock)
            cantidad = producto.cantidad_stock
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
                DetalleVenta(
                    id_venta=None,
                    id_producto=producto_id,
                    cantidad=cantidad,
                    precio_unitario=precio,
                )
            )
            total += subtotal
        
        user_id = None
        if self.user:
            user_id = self.user.id_empleado

        venta = Venta(
            total_venta=total,
            fecha=datetime.combine(datetime.today().date(), datetime.min.time()),
            id_empleado=user_id,
            id_mesa=self.view.mesa.currentData(),
            id_metodo_pago=self.view.metodo_pago.currentData()
        )
        self.db.add(venta)
        self.db.commit()
        venta_id = venta.id_venta

        for detalle in detalles:
            detalle.id_venta = venta_id
            self.db.add(detalle)
            self.db.commit()
        
        for detalle in detalles:
            producto = self.db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
            if producto:
                producto.cantidad_stock -= detalle.cantidad
        
        self.db.commit()

        self.loadSelects()
        self.clear()

    def clear(self):
        self.view.mesa.setCurrentIndex(0)
        self.view.producto.setCurrentIndex(0)
        self.view.cantidad.setValue(0)
        self.view.metodo_pago.setCurrentIndex(0)
        self.view.tableWidget.setRowCount(0)
        self.view.L_total.setText("$ 0.00")
    
    def calcTotal(self):
        total = 0
        for row in range(self.view.tableWidget.rowCount()):
            subtotal = float(self.view.tableWidget.item(row, 3).text())
            total += subtotal
        self.view.L_total.setText("$ " + str(total))