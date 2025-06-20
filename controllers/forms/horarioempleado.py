# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import QDate
from views.forms.HorarioEmpleado_ui import Ui_F_HorarioEmpleado
from models.models import Empleado, HorarioEmpleado, Turno

class logic_HorarioEmpleado(object):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_HorarioEmpleado()
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
        self.view.id_empleado.addItems([str(empleado.nombre) for empleado in self.empleados])
        self.turnos = self.db.query(Turno).all()
        self.view.id_turno.addItems([str(turno.nombre_turno) for turno in self.turnos])
    
    def buildTable(self):
        pass
        # self.columnas = MetodoPago.__table__.columns.keys()
        # self.view.tableWidget.setColumnCount(len(self.columnas))
        # self.view.tableWidget.setHorizontalHeaderLabels(self.columnas)
    
    def populateTable(self):
        pass
        # self.registros = self.db.query(MetodoPago).all()
        # self.view.tableWidget.setRowCount(len(self.registros))
# 
        # for fila_idx, objeto in enumerate(self.registros):
        #     for col_idx, columna in enumerate(self.columnas):
        #         valor = getattr(objeto, columna)
        #         self.view.tableWidget.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def clear(self):
        # self.view.descripcion.clear()
        self.isEdit = False

    def save(self):
        # datasave = MetodoPago(
        #     descripcion = self.view.descripcion.text()
        # )
# 
        # if self.isEdit:
        #     datasave.id_metodo_pago = self.registros[self.view.tableWidget.currentRow()].id_metodo_pago
        #     self.db.merge(datasave)
        # else:
        #     self.db.add(datasave)
        #     
        # self.db.commit()

        self.clear()
        self.populateTable()

    def edit(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
        #     self.view.descripcion.setText(self.registros[actual_row].descripcion)
            self.isEdit = True
    
    def delete(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.db.delete(self.registros[actual_row])
            self.db.commit()
            self.populateTable()
