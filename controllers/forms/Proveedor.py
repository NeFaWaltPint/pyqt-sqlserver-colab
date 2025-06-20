# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import QDate
from views.forms.Proveedor_ui import Ui_F_Proveedor
from models.models import Proveedor

class logic_Proveedor(object):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Proveedor()
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
        self.columnas = Proveedor.__table__.columns.keys()
        self.view.tableWidget.setColumnCount(len(self.columnas))
        self.view.tableWidget.setHorizontalHeaderLabels(self.columnas)
    
    def populateTable(self):
        self.registros = self.db.query(Proveedor).all()
        self.view.tableWidget.setRowCount(len(self.registros))

        for fila_idx, objeto in enumerate(self.registros):
            for col_idx, columna in enumerate(self.columnas):
                valor = getattr(objeto, columna)
                self.view.tableWidget.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def clear(self):
        self.view.nombre.clear()
        self.view.telefono.clear()
        self.view.correo.clear()
        self.view.direccion.clear()
        self.isEdit = False

    def save(self):
        datasave = Proveedor(
            nombre = self.view.nombre.text(),
            telefono = self.view.telefono.text(),
            correo = self.view.correo.text(),
            direccion = self.view.direccion.text()
        )

        if self.isEdit:
            datasave.id_proveedor = self.registros[self.view.tableWidget.currentRow()].id_proveedor
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
            self.view.telefono.setText(self.registros[actual_row].telefono)
            self.view.correo.setText(self.registros[actual_row].correo)
            self.view.direccion.setText(self.registros[actual_row].direccion)
            self.isEdit = True
    
    def delete(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.db.delete(self.registros[actual_row])
            self.db.commit()
            self.populateTable()
