import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit,
    QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy import Integer, String, Date, DateTime, Time, Float, Numeric, Column
from sqlalchemy.orm import DeclarativeMeta, Session
import sys

from controllers.crud import create_record

class DynamicForm(QWidget):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__()
        self.setWindowTitle(f"Formulario: {model_class.__name__}")
        self.model_class = model_class
        self.db = db
        self.inputs = {}  # almacena los widgets por nombre de campo
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        for column in model_class.__table__.columns:
            field_name = column.name
            col_type = column.type
            field_type = type(col_type)

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
            elif isinstance(col_type, (Float, Numeric)):
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

        # Botón de limpiar
        clear_btn = QPushButton("Limpiar")
        clear_btn.clicked.connect(self.clear_form)
        self.layout.addRow(clear_btn)
        # Botón de enviar
        submit_btn = QPushButton("Guardar")
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(submit_btn)

    def fill_from_record(self, record):
        for field, widget in self.inputs.items():
            value = getattr(record, field, None)

            if isinstance(widget, tuple):  # DateTime (QDateEdit + QTimeEdit)
                if isinstance(value, datetime.datetime):
                    widget[0].setDate(QDate(value.date()))
                    widget[1].setTime(QTime(value.time()))
            elif isinstance(widget, QLineEdit):
                widget.setText(str(value) if value is not None else "")
            elif isinstance(widget, QSpinBox):
                widget.setValue(value if value is not None else 0)
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(float(value) if value is not None else 0.0)
            elif isinstance(widget, QDateEdit):
                if isinstance(value, datetime.date):
                    widget.setDate(QDate(value))
            elif isinstance(widget, QTimeEdit):
                if isinstance(value, datetime.time):
                    widget.setTime(QTime(value))

    def clear_form(self):
        for field, widget in self.inputs.items():
            if isinstance(widget, tuple) and isinstance(widget[0], QDateEdit) and isinstance(widget[1], QTimeEdit):
                # DateTime combo
                widget[0].setDate(QDate.currentDate())
                widget[1].setTime(QTime.currentTime())
            elif isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                widget.setValue(0)
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
            elif isinstance(widget, QTimeEdit):
                widget.setTime(QTime.currentTime())

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

            # ❗ Eliminar claves primarias autoincrementales vacías
            for column in self.model_class.__table__.columns:
                if column.primary_key and column.autoincrement:
                    value = data.get(column.name)
                    if not value:  # None, '' o equivalente
                        data.pop(column.name, None)

        QMessageBox.information(self, "Formulario", f"Datos ingresados:\n{data}")

        confirmar = QMessageBox.question(
            self,
            "Confirmar guardado",
            "¿Estas seguro de que deseas guardar este registro?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmar == QMessageBox.StandardButton.Yes:
            try:
                record = create_record(self.db, self.model_class, data)
                QMessageBox.information(self, "Éxito", f"Registro creado Ok")
                self.fill_from_record(record)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar: {str(e)}")
                pass