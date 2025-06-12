from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy.orm import DeclarativeMeta, Session
from views.dynamic_form import DynamicForm
class CompraForm(DynamicForm):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__(model_class, db)
        self.model_class = model_class
        self.db = db
        self.record = None
        self.inputs = {}
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # --- id_compra --- #
        self.id_compra_input = QLineEdit()
        self.id_compra_input.setReadOnly(True)
        self.id_compra_input.setPlaceholderText('Autogenerado')
        self.inputs['id_compra'] = self.id_compra_input
        self.layout.addRow('id_compra (PK)', self.id_compra_input)
        # --- id_proveedor --- #
        self.id_proveedor_input = QSpinBox()
        self.id_proveedor_input.setMaximum(1_000_000)
        self.inputs['id_proveedor'] = self.id_proveedor_input
        self.layout.addRow('id_proveedor', self.id_proveedor_input)
        # --- total_compra --- #
        self.total_compra_input = QDoubleSpinBox()
        self.total_compra_input.setMaximum(1_000_000)
        self.inputs['total_compra'] = self.total_compra_input
        self.layout.addRow('total_compra', self.total_compra_input)
        # --- fecha --- #
        self.fecha_input_date = QDateEdit()
        self.fecha_input_date.setCalendarPopup(True)
        self.fecha_input_date.setDate(QDate.currentDate())
        self.fecha_input_time = QTimeEdit()
        self.fecha_input_time.setTime(QTime.currentTime())
        hbox = QHBoxLayout()
        hbox.addWidget(self.fecha_input_date)
        hbox.addWidget(self.fecha_input_time)
        self.inputs['fecha'] = (self.fecha_input_date, self.fecha_input_time)
        self.layout.addRow('fecha', hbox)

        clear_btn = QPushButton('Limpiar')
        clear_btn.clicked.connect(self.clear_form)
        submit_btn = QPushButton('Guardar')
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(clear_btn)
        self.layout.addRow(submit_btn)