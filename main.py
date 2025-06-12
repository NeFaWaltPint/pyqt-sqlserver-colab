# -*- coding: utf-8 -*-

from controllers.create_drop_db import checkCreateDropDB
from controllers.database import SessionLocal

from models.models import (Base)
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
)

from views.dynamic_form import DynamicForm
from views.list import ListView
from views.static_view_generator import generate_static_code, load_form_from_model

class MainWindow(QMainWindow):
    def __init__(self, model_classes, session):
        super().__init__()
        self.setWindowTitle("Panel de Formularios")
        self.resize(800, 600)

        def handle_lambda_shit(form, sub_tabs):
            return lambda obj: self.formSelecter(obj, form, sub_tabs)
        
        model_tabs = QTabWidget()
        for model in model_classes:
            sub_tabs = QTabWidget()
            list_view = ListView(model, session)
            #form = DynamicForm(model, session)
            form_static = load_form_from_model(model, session)
            
            # code = generate_static_code(model)
            # filename = f"{model.__tablename__}.py"
            # with open("views/forms/" + filename, "w", encoding="utf-8") as f:
            #     f.write(code)
         
            sub_tabs.addTab(list_view, "Datos")
            #sub_tabs.addTab(form, "Formulario")
            sub_tabs.addTab(form_static, "Formulario")
            list_view.registro_seleccionado.connect(
                handle_lambda_shit(form_static, sub_tabs)
            )
            container = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(sub_tabs)
            container.setLayout(layout)
        
            model_tabs.addTab(container, model.__tablename__)

        self.setCentralWidget(model_tabs)
    
    def formSelecter(self, obj, form, sub_tabs):
        form.fill_from_record(obj)
        sub_tabs.setCurrentWidget(form)

def main():

    checkCreateDropDB()

    try:
        # Crear una sesión
        session = SessionLocal()

        app = QApplication(sys.argv)
        window = MainWindow(Base.__subclasses__(), session)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Ups! Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()