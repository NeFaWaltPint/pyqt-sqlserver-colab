# -*- coding: utf-8 -*-

from controllers.create_drop_db import checkCreateDropDB
from controllers.database import SessionLocal
from sqlalchemy import text

from models.models import (Turno, EmpleadoMesa)
import sys
from PyQt6.QtWidgets import (
    QApplication
)

from views.dynamic_form import DynamicForm

def main():

    checkCreateDropDB()

    app = QApplication(sys.argv)
    form1 = DynamicForm(Turno)
    form1.show()
    form2 = DynamicForm(EmpleadoMesa)
    form2.show()
    sys.exit(app.exec())
    # Crear una sesión
    session = SessionLocal()

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