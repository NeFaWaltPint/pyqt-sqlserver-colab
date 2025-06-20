from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget
from views.forms.Venta_ui import Ui_F_Venta

class logic_Venta(object):
    def __init__(self):#, db: Session):
        super().__init__()
        #self.db = db
        self.widget = QWidget()
        self.view = Ui_F_Venta()
        self.view.setupUi(self.widget)

        self.linkActions()
        
    def getView(self):
        return self.widget

    def linkActions(self):
        return

    def save(self):
        print("Guardar")

    def clear(self):
        print("Limpiar")