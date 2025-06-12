from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy.orm import DeclarativeMeta, Session
from views.dynamic_form import DynamicForm
class DetalleCompraForm(DynamicForm):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__(model_class, db)
        self.model_class = model_class
        self.db = db
        self.record = None
        self.inputs = {}
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # --- id_compra --- #
        self.id_compra_input = QSpinBox()
        self.id_compra_input.setMaximum(1_000_000)
        self.inputs['id_compra'] = self.id_compra_input
        self.layout.addRow('id_compra', self.id_compra_input)
        # --- id_producto --- #
        self.id_producto_input = QSpinBox()
        self.id_producto_input.setMaximum(1_000_000)
        self.inputs['id_producto'] = self.id_producto_input
        self.layout.addRow('id_producto', self.id_producto_input)
        # --- cantidad --- #
        self.cantidad_input = QSpinBox()
        self.cantidad_input.setMaximum(1_000_000)
        self.inputs['cantidad'] = self.cantidad_input
        self.layout.addRow('cantidad', self.cantidad_input)
        # --- precio_unitario --- #
        self.precio_unitario_input = QDoubleSpinBox()
        self.precio_unitario_input.setMaximum(1_000_000)
        self.inputs['precio_unitario'] = self.precio_unitario_input
        self.layout.addRow('precio_unitario', self.precio_unitario_input)

        clear_btn = QPushButton('Limpiar')
        clear_btn.clicked.connect(self.clear_form)
        submit_btn = QPushButton('Guardar')
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(clear_btn)
        self.layout.addRow(submit_btn)