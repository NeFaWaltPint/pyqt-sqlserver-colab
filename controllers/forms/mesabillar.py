# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import QDate
from views.forms.MesaBillar_ui import Ui_F_MesaBillar
from models.models import MesaBillar, Empleado

class logic_MesaBillar(object):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_MesaBillar()
        self.view.setupUi(self.widget)

        self.linkActions()
        self.loadSelects()
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
    
    def loadSelects(self):
        self.empleados = self.db.query(Empleado).all()
        self.view.id_empleado.clear()
        self.view.id_empleado.addItem("Seleccione un empleado", userData=None)
        for empleado in self.empleados:
            self.view.id_empleado.addItem(str(empleado.nombre) + " " + str(empleado.apellido), userData=empleado.id_empleado)

    def buildTable(self):
        self.columnas = MesaBillar.__table__.columns.keys()
        self.view.tableWidget.setColumnCount(len(self.columnas))
        self.view.tableWidget.setHorizontalHeaderLabels(self.columnas)
    
    def populateTable(self):
        self.registros = self.db.query(MesaBillar).all()
        self.view.tableWidget.setRowCount(len(self.registros))

        for fila_idx, objeto in enumerate(self.registros):
            for col_idx, columna in enumerate(self.columnas):
                valor = getattr(objeto, columna)
                if columna == "id_empleado":
                    empleado = next((empleado for empleado in self.empleados if empleado.id_empleado == valor), None)
                    valor = str(empleado.nombre) + " " + str(empleado.apellido)
                self.view.tableWidget.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def clear(self):
        self.view.id_empleado.setCurrentIndex(0)
        self.view.estado.setText("")
        self.isEdit = False

    def save(self):
        empleado = self.view.id_empleado.currentData()

        datasave = MesaBillar(
            id_empleado = empleado,
            estado = self.view.estado.text()
        )

        if self.isEdit:
            datasave.id_mesa = self.registros[self.view.tableWidget.currentRow()].id_mesa
            self.db.merge(datasave)
        else:
            self.db.add(datasave)
            
        self.db.commit()

        self.clear()
        self.populateTable()

    def edit(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.view.id_empleado.setCurrentIndex(self.view.id_empleado.findData(self.registros[actual_row].id_empleado))
            self.view.estado.setText(self.registros[actual_row].estado)
            self.isEdit = True
    
    def delete(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.db.delete(self.registros[actual_row])
            self.db.commit()
            self.populateTable()
