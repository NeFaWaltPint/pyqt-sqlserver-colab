from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from controllers.forms.turno import logic_Turno
from controllers.forms.venta import logic_Venta
from views.main_ui import Ui_MainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect buttons
        self.ui.PB_Login.clicked.connect(self.login)

        self.views = []


    def login(self):
        user = self.ui.LE_User.text()
        password = self.ui.LE_Pass.text()
        self.ui.LE_User.setText("")
        self.ui.LE_Pass.setText("")

        if user == "admin" and password == "admin":
            self.views.append(logic_Turno())
            self.ui.Tab_Views.addTab(self.views[-1].getView(), "Turno")
            self.views.append(logic_Venta())
            self.ui.Tab_Views.addTab(self.views[-1].getView(), "Venta")

            self.ui.Tab_Views.setCurrentIndex(1)
            self.ui.Tab_Views.setTabEnabled(0, False)
            return
        
        if user == "empleado" and password == "empleado":
            self.views.append(logic_Venta())
            self.ui.Tab_Views.addTab(self.views[-1].getView(), "Venta")
            self.ui.Tab_Views.setCurrentIndex(1)
            self.ui.Tab_Views.setTabEnabled(0, False)
            return
    
    def injectWidgetinTab(self, someWidget, tabName):
        w = QWidget()
        someWidget.setupUi(w)
        self.ui.Tab_Views.addTab(w, tabName)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
