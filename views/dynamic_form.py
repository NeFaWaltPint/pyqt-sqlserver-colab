from PyQt6.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit,
    QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate, QTime
from sqlalchemy import Integer, String, Date, DateTime, Time, Float, Numeric, Column
from sqlalchemy.orm import DeclarativeMeta
import sys

class DynamicForm(QWidget):
    def __init__(self, model_class: DeclarativeMeta):
        super().__init__()
        self.setWindowTitle(f"Formulario: {model_class.__name__}")
        self.model_class = model_class
        self.inputs = {}  # almacena los widgets por nombre de campo
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        for column in model_class.__table__.columns:
            print(column, column.primary_key, column.autoincrement, column.nullable)
            if column.primary_key and column.autoincrement:
                continue  # omitimos el ID autoincremental

            field_name = column.name
            field_type = type(column.type)

            widget = None
            if field_type in [String]:
                widget = QLineEdit()
            elif field_type in [Integer]:
                widget = QSpinBox()
                widget.setMaximum(1_000_000)
            elif field_type in [Float, Numeric]:
                widget = QDoubleSpinBox()
                widget.setMaximum(1_000_000)
            elif field_type == Date:
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                widget.setDate(QDate.currentDate())
            elif field_type == Time:
                widget = QTimeEdit()
                widget.setTime(QTime.currentTime())
            elif field_type == DateTime:
                widget = QLineEdit()  # podrías crear tu propio selector de datetime

            if widget:
                self.inputs[field_name] = widget
                self.layout.addRow(field_name, widget)

        # Botón de enviar
        submit_btn = QPushButton("Guardar")
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(submit_btn)

    def on_submit(self):
        data = {}
        for field, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                data[field] = widget.text()
            elif isinstance(widget, QSpinBox):
                data[field] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                data[field] = float(widget.value())
            elif isinstance(widget, QDateEdit):
                data[field] = widget.date().toPyDate()
            elif isinstance(widget, QTimeEdit):
                data[field] = widget.time().toPyTime()

        # Aquí podrías usar `crud.create_record(db, self.model_class, data)`
        QMessageBox.information(self, "Formulario", f"Datos ingresados:\n{data}")
