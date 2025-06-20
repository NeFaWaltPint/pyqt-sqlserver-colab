from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from views.main_ui import Ui_MainWindow
import sys
from views.forms.Turno_ui import Ui_F_Turno
from views.forms.Venta_ui import Ui_F_Venta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect buttons
        self.ui.PB_Login.clicked.connect(self.login)


    def login(self):
        user = self.ui.LE_User.text()
        password = self.ui.LE_Pass.text()
        self.ui.LE_User.setText("")
        self.ui.LE_Pass.setText("")

        if user == "admin" and password == "admin":            
            self.ui.Tab_Views.addTab(self.injectWidget(Ui_F_Turno()), "Turno")
            self.ui.Tab_Views.addTab(self.injectWidget(Ui_F_Venta()), "Venta")
            self.ui.Tab_Views.setCurrentIndex(1)
            self.ui.Tab_Views.setTabEnabled(0, False)
            return
        
        if user == "empleado" and password == "empleado":
            self.ui.Tab_Views.addTab(self.injectWidget(Ui_F_Venta()), "Venta")
            self.ui.Tab_Views.setCurrentIndex(1)
            self.ui.Tab_Views.setTabEnabled(0, False)
            return
    
    def injectWidget(self, someWidget):
        w = QWidget()
        someWidget.setupUi(w)
        return w
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
