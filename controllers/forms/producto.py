# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import QDate
from views.forms.Producto_ui import Ui_F_Producto
from models.models import Producto

class logic_Producto(object):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Producto()
        self.view.setupUi(self.widget)

        self.linkActions()
        self.buildTable()
        self.populateTable()
        
        self.isEdit = False
        
    def getView(self):
        return self.widget

    def linkActions(self):
        self.view.PB_Guardar.clicked.connect(self.save)
        self.view.PB_Limpiar.clicked.connect(self.clear)
        self.view.PB_Actualizar.clicked.connect(self.populateTable)
        self.view.PB_Editar.clicked.connect(self.edit)
        self.view.PB_Eliminar.clicked.connect(self.delete)
    
    def buildTable(self):
        self.columnas = Producto.__table__.columns.keys()
        self.view.tableWidget.setColumnCount(len(self.columnas))
        self.view.tableWidget.setHorizontalHeaderLabels(self.columnas)
    
    def populateTable(self):
        self.registros = self.db.query(Producto).all()
        self.view.tableWidget.setRowCount(len(self.registros))

        for fila_idx, objeto in enumerate(self.registros):
            for col_idx, columna in enumerate(self.columnas):
                valor = getattr(objeto, columna)
                self.view.tableWidget.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def clear(self):
        self.view.nombre.clear()
        self.view.categoria.clear()
        self.view.unidad_medida.clear()
        self.view.precio_compra.setValue(0.0)
        self.view.precio_venta.setValue(0)
        self.view.cantidad_stock.setValue(0)
        self.isEdit = False

    def save(self):
        datasave = Producto(
            nombre = self.view.nombre.text(),
            categoria = self.view.categoria.text(),
            unidad_medida = self.view.unidad_medida.text(),
            precio_compra = self.view.precio_compra.value(),
            precio_venta = self.view.precio_venta.value(),
            cantidad_stock = self.view.cantidad_stock.value()
        )

        if self.isEdit:
            datasave.id_producto = self.registros[self.view.tableWidget.currentRow()].id_producto
            self.db.merge(datasave)
        else:
            self.db.add(datasave)
            
        self.db.commit()

        self.clear()
        self.populateTable()

    def edit(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.view.nombre.setText(self.registros[actual_row].nombre)
            self.view.categoria.setText(self.registros[actual_row].categoria)
            self.view.unidad_medida.setText(self.registros[actual_row].unidad_medida)
            self.view.precio_compra.setValue(self.registros[actual_row].precio_compra)
            self.view.precio_venta.setValue(self.registros[actual_row].precio_venta)
            self.view.cantidad_stock.setValue(self.registros[actual_row].cantidad_stock)
            self.isEdit = True
    
    def delete(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.db.delete(self.registros[actual_row])
            self.db.commit()
            self.populateTable()
