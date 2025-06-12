from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy.orm import DeclarativeMeta, Session
from views.dynamic_form import DynamicForm
class MetodoPagoForm(DynamicForm):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__(model_class, db)
        self.model_class = model_class
        self.db = db
        self.record = None
        self.inputs = {}
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # --- id_metodo_pago --- #
        self.id_metodo_pago_input = QLineEdit()
        self.id_metodo_pago_input.setReadOnly(True)
        self.id_metodo_pago_input.setPlaceholderText('Autogenerado')
        self.inputs['id_metodo_pago'] = self.id_metodo_pago_input
        self.layout.addRow('id_metodo_pago (PK)', self.id_metodo_pago_input)
        # --- descripcion --- #
        self.descripcion_input = QLineEdit()
        self.inputs['descripcion'] = self.descripcion_input
        self.layout.addRow('descripcion', self.descripcion_input)

        clear_btn = QPushButton('Limpiar')
        clear_btn.clicked.connect(self.clear_form)
        submit_btn = QPushButton('Guardar')
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(clear_btn)
        self.layout.addRow(submit_btn)