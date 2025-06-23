# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import QDate
from views.forms.Juego_ui import Ui_F_Juego
from models.models import Juego, MesaBillar

class logic_Juego(object):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Juego()
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
        self.mesas = self.db.query(MesaBillar).all()
        self.view.id_mesa.clear()
        self.view.id_mesa.addItem("Seleccione una mesa", userData=None)
        for mesa in self.mesas:
            self.view.id_mesa.addItem(str(mesa.id_mesa) + " - " + str(mesa.estado), userData=mesa.id_mesa)

    def buildTable(self):
        self.columnas = Juego.__table__.columns.keys()
        self.view.tableWidget.setColumnCount(len(self.columnas))
        self.view.tableWidget.setHorizontalHeaderLabels(self.columnas)
    
    def populateTable(self):
        self.registros = self.db.query(Juego).all()
        self.view.tableWidget.setRowCount(len(self.registros))

        for fila_idx, objeto in enumerate(self.registros):
            for col_idx, columna in enumerate(self.columnas):
                valor = getattr(objeto, columna)
                self.view.tableWidget.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def clear(self):
        self.view.id_mesa.setCurrentIndex(0)
        self.view.fecha_inicio.setDate(QDate(2000, 1, 1))
        self.view.fecha_fin.setDate(QDate(2000, 1, 1))
        self.view.total_juegos.setValue(0)
        self.isEdit = False

    def save(self):
        mesa = self.view.id_mesa.currentData()

        datasave = Juego(
            id_mesa = mesa,
            fecha_inicio = datetime.combine(self.view.fecha_inicio.date().toPyDate(), datetime.min.time()),
            fecha_fin = datetime.combine(self.view.fecha_fin.date().toPyDate(), datetime.min.time()),
            total_juegos = self.view.total_juegos.value()
        )

        if self.isEdit:
            datasave.id_juego = self.registros[self.view.tableWidget.currentRow()].id_juego
            self.db.merge(datasave)
        else:
            self.db.add(datasave)
            
        self.db.commit()

        self.clear()
        self.populateTable()

    def edit(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.view.id_mesa.setCurrentIndex(self.view.id_mesa.findData(self.registros[actual_row].id_mesa))
            self.view.fecha_inicio.setDate(self.registros[actual_row].fecha_inicio)
            self.view.fecha_fin.setDate(self.registros[actual_row].fecha_fin)
            self.view.total_juegos.setValue(self.registros[actual_row].total_juegos)
            self.isEdit = True
    
    def delete(self):
        actual_row = self.view.tableWidget.currentRow()
        if actual_row >= 0 and actual_row < len(self.registros):
            self.db.delete(self.registros[actual_row])
            self.db.commit()
            self.populateTable()
