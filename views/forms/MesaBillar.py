from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy.orm import DeclarativeMeta, Session
from views.dynamic_form import DynamicForm
class MesaBillarForm(DynamicForm):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__(model_class, db)
        self.model_class = model_class
        self.db = db
        self.record = None
        self.inputs = {}
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # --- id_mesa --- #
        self.id_mesa_input = QLineEdit()
        self.id_mesa_input.setReadOnly(True)
        self.id_mesa_input.setPlaceholderText('Autogenerado')
        self.inputs['id_mesa'] = self.id_mesa_input
        self.layout.addRow('id_mesa (PK)', self.id_mesa_input)
        # --- id_empleado --- #
        self.id_empleado_input = QSpinBox()
        self.id_empleado_input.setMaximum(1_000_000)
        self.inputs['id_empleado'] = self.id_empleado_input
        self.layout.addRow('id_empleado', self.id_empleado_input)
        # --- estado --- #
        self.estado_input = QLineEdit()
        self.inputs['estado'] = self.estado_input
        self.layout.addRow('estado', self.estado_input)

        clear_btn = QPushButton('Limpiar')
        clear_btn.clicked.connect(self.clear_form)
        submit_btn = QPushButton('Guardar')
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(clear_btn)
        self.layout.addRow(submit_btn)