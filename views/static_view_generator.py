from sqlalchemy import Float, Numeric

def generate_static_code(model_class):
    class_name = f"{model_class.__name__}Form"
    lines = []
    lines.append("from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QHBoxLayout, QPushButton, QMessageBox")
    lines.append("from PyQt6.QtCore import QDate, QTime, QDateTime")
    lines.append("from sqlalchemy.orm import DeclarativeMeta, Session")
    lines.append("from views.dynamic_form import DynamicForm")

    lines.append(f"class {class_name}(DynamicForm):")
    lines.append("    def __init__(self, model_class: DeclarativeMeta, db: Session):")
    lines.append("        super().__init__(model_class, db)")
    lines.append("        self.model_class = model_class")
    lines.append("        self.db = db")
    lines.append("        self.record = None")
    lines.append("        self.inputs = {}")
    lines.append("        self.layout = QFormLayout()")
    lines.append("        self.setLayout(self.layout)")
    lines.append("")

    for column in model_class.__table__.columns:
        field_name = column.name
        col_type = column.type
        field_type = type(col_type)

        widget_name = f"{field_name}_input"
        lines.append(f"        # --- {field_name} --- #")

        if column.primary_key and column.autoincrement:
            lines.append(f"        self.{widget_name} = QLineEdit()")
            lines.append(f"        self.{widget_name}.setReadOnly(True)")
            lines.append(f"        self.{widget_name}.setPlaceholderText('Autogenerado')")
            lines.append(f"        self.inputs['{field_name}'] = self.{widget_name}")
            lines.append(f"        self.layout.addRow('{field_name} (PK)', self.{widget_name})")
            continue

        if field_type.__name__ == "String":
            lines.append(f"        self.{widget_name} = QLineEdit()")
        elif field_type.__name__ == "Integer":
            lines.append(f"        self.{widget_name} = QSpinBox()")
            lines.append(f"        self.{widget_name}.setMaximum(1_000_000)")
        elif isinstance(col_type, (Float, Numeric)):
            lines.append(f"        self.{widget_name} = QDoubleSpinBox()")
            lines.append(f"        self.{widget_name}.setMaximum(1_000_000)")
        elif field_type.__name__ == "Date":
            lines.append(f"        self.{widget_name} = QDateEdit()")
            lines.append(f"        self.{widget_name}.setCalendarPopup(True)")
            lines.append(f"        self.{widget_name}.setDate(QDate.currentDate())")
        elif field_type.__name__ == "Time":
            lines.append(f"        self.{widget_name} = QTimeEdit()")
            lines.append(f"        self.{widget_name}.setTime(QTime.currentTime())")
        elif field_type.__name__ == "DateTime":
            lines.append(f"        self.{widget_name}_date = QDateEdit()")
            lines.append(f"        self.{widget_name}_date.setCalendarPopup(True)")
            lines.append(f"        self.{widget_name}_date.setDate(QDate.currentDate())")
            lines.append(f"        self.{widget_name}_time = QTimeEdit()")
            lines.append(f"        self.{widget_name}_time.setTime(QTime.currentTime())")
            lines.append(f"        hbox = QHBoxLayout()")
            lines.append(f"        hbox.addWidget(self.{widget_name}_date)")
            lines.append(f"        hbox.addWidget(self.{widget_name}_time)")
            lines.append(f"        self.inputs['{field_name}'] = (self.{widget_name}_date, self.{widget_name}_time)")
            lines.append(f"        self.layout.addRow('{field_name}', hbox)")
            continue
        else:
            continue

        lines.append(f"        self.inputs['{field_name}'] = self.{widget_name}")
        lines.append(f"        self.layout.addRow('{field_name}', self.{widget_name})")

    lines.append("")
    lines.append("        clear_btn = QPushButton('Limpiar')")
    lines.append("        clear_btn.clicked.connect(self.clear_form)")
    lines.append("        submit_btn = QPushButton('Guardar')")
    lines.append("        submit_btn.clicked.connect(self.on_submit)")
    lines.append("        self.layout.addRow(clear_btn)")
    lines.append("        self.layout.addRow(submit_btn)")

    return "\n".join(lines)

import importlib
def load_form_from_model(model_class, session):
    tablename = model_class.__tablename__
    module_name = f"views.forms.{tablename}"
    class_name = f"{model_class.__name__}Form"
    module = importlib.import_module(module_name)
    form_class = getattr(module, class_name)
    return form_class(model_class, session)