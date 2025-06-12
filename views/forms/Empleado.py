from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy.orm import DeclarativeMeta, Session
from views.dynamic_form import DynamicForm
class EmpleadoForm(DynamicForm):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__(model_class, db)
        self.model_class = model_class
        self.db = db
        self.record = None
        self.inputs = {}
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # --- id_empleado --- #
        self.id_empleado_input = QLineEdit()
        self.id_empleado_input.setReadOnly(True)
        self.id_empleado_input.setPlaceholderText('Autogenerado')
        self.inputs['id_empleado'] = self.id_empleado_input
        self.layout.addRow('id_empleado (PK)', self.id_empleado_input)
        # --- nombre --- #
        self.nombre_input = QLineEdit()
        self.inputs['nombre'] = self.nombre_input
        self.layout.addRow('nombre', self.nombre_input)
        # --- apellido --- #
        self.apellido_input = QLineEdit()
        self.inputs['apellido'] = self.apellido_input
        self.layout.addRow('apellido', self.apellido_input)
        # --- salario --- #
        self.salario_input = QDoubleSpinBox()
        self.salario_input.setMaximum(1_000_000)
        self.inputs['salario'] = self.salario_input
        self.layout.addRow('salario', self.salario_input)
        # --- fecha_ingreso --- #
        self.fecha_ingreso_input = QDateEdit()
        self.fecha_ingreso_input.setCalendarPopup(True)
        self.fecha_ingreso_input.setDate(QDate.currentDate())
        self.inputs['fecha_ingreso'] = self.fecha_ingreso_input
        self.layout.addRow('fecha_ingreso', self.fecha_ingreso_input)

        clear_btn = QPushButton('Limpiar')
        clear_btn.clicked.connect(self.clear_form)
        submit_btn = QPushButton('Guardar')
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(clear_btn)
        self.layout.addRow(submit_btn)