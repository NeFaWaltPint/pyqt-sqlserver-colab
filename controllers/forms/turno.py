# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget
from views.forms.Turno_ui import Ui_F_Turno

class logic_Turno(object):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Turno()
        self.view.setupUi(self.widget)

        self.linkActions()
        
    def getView(self):
        return self.widget

    def linkActions(self):
        self.view.PB_Guardar.clicked.connect(self.save)
        self.view.PB_Limpiar.clicked.connect(self.clear)

    def save(self):
        print("Guardar")

    def clear(self):
        print("Limpiar")