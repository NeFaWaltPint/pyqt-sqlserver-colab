# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import QDate
from views.forms.Turno_ui import Ui_F_Turno
from models.models import Turno

class logic_Turno(object):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Turno()
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
        self.columnas = Turno.__table__.columns.keys()
        self.view.tableWidget.setColumnCount(len(self.columnas))
        self.view.tableWidget.setHorizontalHeaderLabels(self.columnas)
    
    def populateTable(self):
        self.registros = self.db.query(Turno).all()
        self.view.tableWidget.setRowCount(len(self.registros))

        for fila_idx, objeto in enumerate(self.registros):
            for col_idx, columna in enumerate(self.columnas):
                valor = getattr(objeto, columna)
                self.view.tableWidget.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def clear(self):
        self.view.nombre_turno.clear()
        self.view.fecha_inicio.setDate(QDate(2000, 1, 1))
        self.view.fecha_fin.setDate(QDate(2000, 1, 1))
        self.isEdit = False

    def save(self):
        turno = Turno(
            nombre_turno=self.view.nombre_turno.text(),
            fecha_inicio=datetime.combine(self.view.fecha_inicio.date().toPyDate(), datetime.min.time()),
            fecha_fin=datetime.combine(self.view.fecha_fin.date().toPyDate(), datetime.min.time())
        )

        if self.isEdit:
            turno.id_turno = self.registros[self.view.tableWidget.currentRow()].id_turno    
            self.db.merge(turno)
        else:
            self.db.add(turno)
            
        self.db.commit()

        self.clear()
        self.populateTable()

    def edit(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.view.nombre_turno.setText(self.registros[actual_row].nombre_turno)
            self.view.fecha_inicio.setDate(self.registros[actual_row].fecha_inicio)
            self.view.fecha_fin.setDate(self.registros[actual_row].fecha_fin)
            self.isEdit = True
    
    def delete(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.db.delete(self.registros[actual_row])
            self.db.commit()
            self.populateTable()
