from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy.orm import DeclarativeMeta, Session
from views.dynamic_form import DynamicForm
class ProductoForm(DynamicForm):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__(model_class, db)
        self.model_class = model_class
        self.db = db
        self.record = None
        self.inputs = {}
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # --- id_producto --- #
        self.id_producto_input = QLineEdit()
        self.id_producto_input.setReadOnly(True)
        self.id_producto_input.setPlaceholderText('Autogenerado')
        self.inputs['id_producto'] = self.id_producto_input
        self.layout.addRow('id_producto (PK)', self.id_producto_input)
        # --- nombre --- #
        self.nombre_input = QLineEdit()
        self.inputs['nombre'] = self.nombre_input
        self.layout.addRow('nombre', self.nombre_input)
        # --- categoria --- #
        self.categoria_input = QLineEdit()
        self.inputs['categoria'] = self.categoria_input
        self.layout.addRow('categoria', self.categoria_input)
        # --- unidad_medida --- #
        self.unidad_medida_input = QLineEdit()
        self.inputs['unidad_medida'] = self.unidad_medida_input
        self.layout.addRow('unidad_medida', self.unidad_medida_input)
        # --- precio_compra --- #
        self.precio_compra_input = QDoubleSpinBox()
        self.precio_compra_input.setMaximum(1_000_000)
        self.inputs['precio_compra'] = self.precio_compra_input
        self.layout.addRow('precio_compra', self.precio_compra_input)
        # --- precio_venta --- #
        self.precio_venta_input = QDoubleSpinBox()
        self.precio_venta_input.setMaximum(1_000_000)
        self.inputs['precio_venta'] = self.precio_venta_input
        self.layout.addRow('precio_venta', self.precio_venta_input)
        # --- cantidad_stock --- #
        self.cantidad_stock_input = QSpinBox()
        self.cantidad_stock_input.setMaximum(1_000_000)
        self.inputs['cantidad_stock'] = self.cantidad_stock_input
        self.layout.addRow('cantidad_stock', self.cantidad_stock_input)

        clear_btn = QPushButton('Limpiar')
        clear_btn.clicked.connect(self.clear_form)
        submit_btn = QPushButton('Guardar')
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(clear_btn)
        self.layout.addRow(submit_btn)