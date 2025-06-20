from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from sqlalchemy.orm import DeclarativeMeta, Session
from controllers.crud import get_all_records, delete_record

class ListView(QWidget):
    registro_seleccionado = pyqtSignal(object)  # Para enviar el objeto seleccionado al formulario

    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__()
        self.setWindowTitle(f"Tabla de: {model_class.__name__}")
        self.model_class = model_class
        self.db = db

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.layout.addWidget(self.table)

        # Botones
        refresh_button = QPushButton("Actualizar Lista")
        new_button = QPushButton("Nuevo Registro")
        edit_button = QPushButton("Editar Seleccionado")
        delete_button = QPushButton("Eliminar Seleccionado")

        refresh_button.clicked.connect(self.populate_table)
        new_button.clicked.connect(self.new_register)
        edit_button.clicked.connect(self.select_for_editing)
        delete_button.clicked.connect(self.delete_selected_row)

        self.layout.addWidget(refresh_button)
        self.layout.addWidget(new_button)
        self.layout.addWidget(edit_button)
        self.layout.addWidget(delete_button)

        self.populate_table()

    def populate_table(self):
        columnas = self.model_class.__table__.columns.keys()
        registros = get_all_records(self.db, self.model_class)

        self.table.setRowCount(len(registros))
        self.table.setColumnCount(len(columnas))
        self.table.setHorizontalHeaderLabels(columnas)
        self.objetos = registros

        for fila_idx, objeto in enumerate(registros):
            for col_idx, columna in enumerate(columnas):
                valor = getattr(objeto, columna)
                self.table.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def get_selected_object(self):
        selected = self.table.currentRow()
        if selected >= 0 and selected < len(self.objetos):
            return self.objetos[selected]
        return None

    def delete_selected_row(self):
        obj = self.get_selected_object()
        if obj:
            confirm = QMessageBox.question(
                self, "Confirmar eliminación",
                "¿Eliminar este registro?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                delete_record(self.db, self.model_class, record_obj=obj)
                self.populate_table()
        else:
            QMessageBox.warning(self, "Sin selección", "Selecciona un registro para eliminar.")

    def select_for_editing(self):
        obj = self.get_selected_object()
        if obj:
            self.registro_seleccionado.emit(obj)
        else:
            QMessageBox.warning(self, "Sin selección", "Selecciona un registro para editar.")

    def new_register(self):
        self.registro_seleccionado.emit(None)