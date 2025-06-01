from PyQt6.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit,
    QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import QDate, QTime, QDateTime
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
            field_name = column.name
            field_type = type(column.type)

            # Caso especial: clave primaria autoincremental → solo lectura
            if column.primary_key and column.autoincrement:
                widget = QLineEdit()
                widget.setReadOnly(True)
                widget.setPlaceholderText("Autogenerado")
                self.inputs[field_name] = widget
                self.layout.addRow(f"{field_name} (PK)", widget)
                continue

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
                # Usamos QDateEdit + QTimeEdit en una fila horizontal
                date_widget = QDateEdit()
                date_widget.setCalendarPopup(True)
                date_widget.setDate(QDate.currentDate())

                time_widget = QTimeEdit()
                time_widget.setTime(QTime.currentTime())

                container = QWidget()
                hbox = QHBoxLayout()
                hbox.addWidget(date_widget)
                hbox.addWidget(time_widget)
                hbox.setContentsMargins(0, 0, 0, 0)
                container.setLayout(hbox)

                # Guardamos como tupla para extraer luego
                self.inputs[field_name] = (date_widget, time_widget)
                self.layout.addRow(field_name, container)
                continue  # ya añadimos el layout, no añadir más abajo

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
            if isinstance(widget, tuple) and isinstance(widget[0], QDateEdit) and isinstance(widget[1], QTimeEdit):
                # Caso DateTime
                qdate = widget[0].date()
                qtime = widget[1].time()
                data[field] = QDateTime(qdate, qtime).toPyDateTime()
            elif isinstance(widget, QLineEdit):
                data[field] = widget.text()
            elif isinstance(widget, QSpinBox):
                data[field] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                data[field] = float(widget.value())
            elif isinstance(widget, QDateEdit):
                data[field] = widget.date().toPyDate()
            elif isinstance(widget, QTimeEdit):
                data[field] = widget.time().toPyTime()

        # Mostrar los datos
        QMessageBox.information(self, "Formulario", f"Datos ingresados:\n{data}")
