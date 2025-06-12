from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy.orm import DeclarativeMeta, Session
from views.dynamic_form import DynamicForm
class TurnoForm(DynamicForm):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__(model_class, db)
        self.model_class = model_class
        self.db = db
        self.record = None
        self.inputs = {}
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # --- id_turno --- #
        self.id_turno_input = QLineEdit()
        self.id_turno_input.setReadOnly(True)
        self.id_turno_input.setPlaceholderText('Autogenerado')
        self.inputs['id_turno'] = self.id_turno_input
        self.layout.addRow('id_turno (PK)', self.id_turno_input)
        # --- nombre_turno --- #
        self.nombre_turno_input = QLineEdit()
        self.inputs['nombre_turno'] = self.nombre_turno_input
        self.layout.addRow('nombre_turno', self.nombre_turno_input)
        # --- fecha_inicio --- #
        self.fecha_inicio_input_date = QDateEdit()
        self.fecha_inicio_input_date.setCalendarPopup(True)
        self.fecha_inicio_input_date.setDate(QDate.currentDate())
        self.fecha_inicio_input_time = QTimeEdit()
        self.fecha_inicio_input_time.setTime(QTime.currentTime())
        hbox = QHBoxLayout()
        hbox.addWidget(self.fecha_inicio_input_date)
        hbox.addWidget(self.fecha_inicio_input_time)
        self.inputs['fecha_inicio'] = (self.fecha_inicio_input_date, self.fecha_inicio_input_time)
        self.layout.addRow('fecha_inicio', hbox)
        # --- fecha_fin --- #
        self.fecha_fin_input_date = QDateEdit()
        self.fecha_fin_input_date.setCalendarPopup(True)
        self.fecha_fin_input_date.setDate(QDate.currentDate())
        self.fecha_fin_input_time = QTimeEdit()
        self.fecha_fin_input_time.setTime(QTime.currentTime())
        hbox = QHBoxLayout()
        hbox.addWidget(self.fecha_fin_input_date)
        hbox.addWidget(self.fecha_fin_input_time)
        self.inputs['fecha_fin'] = (self.fecha_fin_input_date, self.fecha_fin_input_time)
        self.layout.addRow('fecha_fin', hbox)

        clear_btn = QPushButton('Limpiar')
        clear_btn.clicked.connect(self.clear_form)
        submit_btn = QPushButton('Guardar')
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(clear_btn)
        self.layout.addRow(submit_btn)