# -*- coding: utf-8 -*-

from controllers.create_drop_db import checkCreateDropDB
from controllers.database import SessionLocal
from sqlalchemy import text

from models.models import (Base, Turno, EmpleadoMesa)
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget
)

from views.dynamic_form import DynamicForm

class MainWindow(QMainWindow):
    def __init__(self, model_classes, session):
        super().__init__()
        self.setWindowTitle("Panel de Formularios")

        tabs = QTabWidget()
        for model in model_classes:
            form = DynamicForm(model, session)
            tabs.addTab(form, model.__tablename__)
        self.setCentralWidget(tabs)

def main():

    checkCreateDropDB()

    # Crear una sesión
    session = SessionLocal()

    app = QApplication(sys.argv)
    window = MainWindow(Base.__subclasses__(), session)
    window.show()
    sys.exit(app.exec())

    try:
        result = session.execute(text("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """))
        for row in result:
            print(f" - {row[0]}")
    except Exception as e:
        print(f"Ups! Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()