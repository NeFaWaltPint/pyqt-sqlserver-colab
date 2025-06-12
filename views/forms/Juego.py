from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy.orm import DeclarativeMeta, Session
from views.dynamic_form import DynamicForm
class JuegoForm(DynamicForm):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__(model_class, db)
        self.model_class = model_class
        self.db = db
        self.record = None
        self.inputs = {}
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # --- id_juego --- #
        self.id_juego_input = QLineEdit()
        self.id_juego_input.setReadOnly(True)
        self.id_juego_input.setPlaceholderText('Autogenerado')
        self.inputs['id_juego'] = self.id_juego_input
        self.layout.addRow('id_juego (PK)', self.id_juego_input)
        # --- id_mesa --- #
        self.id_mesa_input = QSpinBox()
        self.id_mesa_input.setMaximum(1_000_000)
        self.inputs['id_mesa'] = self.id_mesa_input
        self.layout.addRow('id_mesa', self.id_mesa_input)
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
        # --- total_juegos --- #
        self.total_juegos_input = QDoubleSpinBox()
        self.total_juegos_input.setMaximum(1_000_000)
        self.inputs['total_juegos'] = self.total_juegos_input
        self.layout.addRow('total_juegos', self.total_juegos_input)

        clear_btn = QPushButton('Limpiar')
        clear_btn.clicked.connect(self.clear_form)
        submit_btn = QPushButton('Guardar')
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(clear_btn)
        self.layout.addRow(submit_btn)