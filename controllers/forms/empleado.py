
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import QDate
from views.forms.Empleado_ui import Ui_F_Empleado
from models.models import Empleado

class logic_Empleado(object):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Empleado()
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
        self.columnas = Empleado.__table__.columns.keys()
        self.view.tableWidget.setColumnCount(len(self.columnas))
        self.view.tableWidget.setHorizontalHeaderLabels(self.columnas)
    
    def populateTable(self):
        self.registros = self.db.query(Empleado).all()
        self.view.tableWidget.setRowCount(len(self.registros))

        for fila_idx, objeto in enumerate(self.registros):
            for col_idx, columna in enumerate(self.columnas):
                valor = getattr(objeto, columna)
                self.view.tableWidget.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def clear(self):
        self.view.nombre.clear()
        self.view.apellido.clear()
        self.view.salario.setValue(0)
        self.view.fecha_ingreso.setDate(QDate(2000, 1, 1))
        self.isEdit = False

    def save(self):
        datasave = Empleado(
            nombre = self.view.nombre.text(),
            apellido = self.view.apellido.text(),
            salario = self.view.salario.value(),
            fecha_ingreso = datetime.combine(self.view.fecha_ingreso.date().toPyDate(), datetime.min.time())
        )

        if self.isEdit:
            datasave.id_empleado = self.registros[self.view.tableWidget.currentRow()].id_empleado    
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
            self.view.apellido.setText(self.registros[actual_row].apellido)
            self.view.salario.setValue(self.registros[actual_row].salario)
            self.view.fecha_ingreso.setDate(self.registros[actual_row].fecha_ingreso)
            self.isEdit = True
    
    def delete(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.db.delete(self.registros[actual_row])
            self.db.commit()
            self.populateTable()
