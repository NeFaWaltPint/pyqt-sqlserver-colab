from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy.orm import DeclarativeMeta, Session
from views.dynamic_form import DynamicForm
class ProveedorForm(DynamicForm):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__(model_class, db)
        self.model_class = model_class
        self.db = db
        self.record = None
        self.inputs = {}
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # --- id_proveedor --- #
        self.id_proveedor_input = QLineEdit()
        self.id_proveedor_input.setReadOnly(True)
        self.id_proveedor_input.setPlaceholderText('Autogenerado')
        self.inputs['id_proveedor'] = self.id_proveedor_input
        self.layout.addRow('id_proveedor (PK)', self.id_proveedor_input)
        # --- nombre --- #
        self.nombre_input = QLineEdit()
        self.inputs['nombre'] = self.nombre_input
        self.layout.addRow('nombre', self.nombre_input)
        # --- telefono --- #
        self.telefono_input = QLineEdit()
        self.inputs['telefono'] = self.telefono_input
        self.layout.addRow('telefono', self.telefono_input)
        # --- correo --- #
        self.correo_input = QLineEdit()
        self.inputs['correo'] = self.correo_input
        self.layout.addRow('correo', self.correo_input)
        # --- direccion --- #
        self.direccion_input = QLineEdit()
        self.inputs['direccion'] = self.direccion_input
        self.layout.addRow('direccion', self.direccion_input)

        clear_btn = QPushButton('Limpiar')
        clear_btn.clicked.connect(self.clear_form)
        submit_btn = QPushButton('Guardar')
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(clear_btn)
        self.layout.addRow(submit_btn)