from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QDate, QTime, QDateTime
from sqlalchemy.orm import DeclarativeMeta, Session
from views.dynamic_form import DynamicForm
class VentaForm(DynamicForm):
    def __init__(self, model_class: DeclarativeMeta, db: Session):
        super().__init__(model_class, db)
        self.model_class = model_class
        self.db = db
        self.record = None
        self.inputs = {}
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # --- id_venta --- #
        self.id_venta_input = QLineEdit()
        self.id_venta_input.setReadOnly(True)
        self.id_venta_input.setPlaceholderText('Autogenerado')
        self.inputs['id_venta'] = self.id_venta_input
        self.layout.addRow('id_venta (PK)', self.id_venta_input)
        # --- total_venta --- #
        self.total_venta_input = QDoubleSpinBox()
        self.total_venta_input.setMaximum(1_000_000)
        self.inputs['total_venta'] = self.total_venta_input
        self.layout.addRow('total_venta', self.total_venta_input)
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
        # --- id_empleado --- #
        self.id_empleado_input = QSpinBox()
        self.id_empleado_input.setMaximum(1_000_000)
        self.inputs['id_empleado'] = self.id_empleado_input
        self.layout.addRow('id_empleado', self.id_empleado_input)
        # --- id_mesa --- #
        self.id_mesa_input = QSpinBox()
        self.id_mesa_input.setMaximum(1_000_000)
        self.inputs['id_mesa'] = self.id_mesa_input
        self.layout.addRow('id_mesa', self.id_mesa_input)
        # --- id_metodo_pago --- #
        self.id_metodo_pago_input = QSpinBox()
        self.id_metodo_pago_input.setMaximum(1_000_000)
        self.inputs['id_metodo_pago'] = self.id_metodo_pago_input
        self.layout.addRow('id_metodo_pago', self.id_metodo_pago_input)

        clear_btn = QPushButton('Limpiar')
        clear_btn.clicked.connect(self.clear_form)
        submit_btn = QPushButton('Guardar')
        submit_btn.clicked.connect(self.on_submit)
        self.layout.addRow(clear_btn)
        self.layout.addRow(submit_btn)