from sqlalchemy import Column, Integer, String, Date, Time, DateTime, DECIMAL, ForeignKey, CHAR
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Turno(Base):
    __tablename__ = 'Turno'
    id_turno = Column(Integer, primary_key=True)
    nombre_turno = Column(String(100))
    dia = Column(String(20))
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    empleados = relationship("HorarioEmpleado", back_populates="turno")


class MetodoPago(Base):
    __tablename__ = 'MetodoPago'
    id_metodo_pago = Column(Integer, primary_key=True)
    descripcion = Column(String(100))
    ventas = relationship("Venta", back_populates="metodo_pago")


class Empleado(Base):
    __tablename__ = 'Empleado'
    id_empleado = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    salario = Column(DECIMAL(14, 2))
    fecha_ingreso = Column(Date)
    pagos = relationship("PagoSalario", back_populates="empleado")
    usos_mesa = relationship("UsoMesaBillar", back_populates="empleado")
    ventas = relationship("Venta", back_populates="empleado")
    horarios = relationship("HorarioEmpleado", back_populates="empleado")


class PagoSalario(Base):
    __tablename__ = 'PagoSalario'
    id_pago = Column(Integer, primary_key=True)
    id_empleado = Column(Integer, ForeignKey('Empleado.id_empleado'))
    fecha_pago = Column(Date)
    monto_pagado = Column(DECIMAL(14, 2))
    empleado = relationship("Empleado", back_populates="pagos")


class Proveedor(Base):
    __tablename__ = 'Proveedor'
    id_proveedor = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    telefono = Column(String(20))
    correo = Column(String(100))
    direccion = Column(String(200))
    compras = relationship("Compra", back_populates="proveedor")


class Producto(Base):
    __tablename__ = 'Producto'
    id_producto = Column(Integer, primary_key=True)
    nombre = Column(CHAR(50))
    categoria = Column(CHAR(50))
    unidad_medida = Column(CHAR(50))
    precio_compra = Column(DECIMAL(14, 2))
    precio_venta = Column(DECIMAL(14, 2))
    stock_actual = Column(Integer)
    detalles_compra = relationship("DetalleCompra", back_populates="producto")
    detalles_venta = relationship("DetalleVenta", back_populates="producto")


class Compra(Base):
    __tablename__ = 'Compra'
    id_compra = Column(Integer, primary_key=True)
    id_proveedor = Column(Integer, ForeignKey('Proveedor.id_proveedor'))
    total_compra = Column(DECIMAL(14, 2))
    fecha = Column(Date)
    proveedor = relationship("Proveedor", back_populates="compras")
    detalles = relationship("DetalleCompra", back_populates="compra")


class DetalleCompra(Base):
    __tablename__ = 'DetalleCompra'
    id_compra = Column(Integer, ForeignKey('Compra.id_compra'), primary_key=True)
    id_producto = Column(Integer, ForeignKey('Producto.id_producto'), primary_key=True)
    cantidad = Column(Integer)
    precio_unitario = Column(DECIMAL(14, 2))
    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_compra")


class MesaBillar(Base):
    __tablename__ = 'MesaBillar'
    id_mesa = Column(Integer, primary_key=True)
    estado = Column(String(20))
    usos = relationship("UsoMesaBillar", back_populates="mesa")


class UsoMesaBillar(Base):
    __tablename__ = 'UsoMesaBillar'
    id_uso_mesa = Column(Integer, primary_key=True)
    id_mesa = Column(Integer, ForeignKey('MesaBillar.id_mesa'))
    id_empleado = Column(Integer, ForeignKey('Empleado.id_empleado'))
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    numero_juegos = Column(Integer)
    mesa = relationship("MesaBillar", back_populates="usos")
    empleado = relationship("Empleado", back_populates="usos_mesa")
    ventas = relationship("Venta", back_populates="uso_mesa")


class Venta(Base):
    __tablename__ = 'Venta'
    id_venta = Column(Integer, primary_key=True)
    total_venta = Column(DECIMAL(14, 2))
    fecha = Column(DateTime)
    id_empleado = Column(Integer, ForeignKey('Empleado.id_empleado'))
    id_uso_mesa = Column(Integer, ForeignKey('UsoMesaBillar.id_uso_mesa'))
    id_metodo_pago = Column(Integer, ForeignKey('MetodoPago.id_metodo_pago'))
    empleado = relationship("Empleado", back_populates="ventas")
    uso_mesa = relationship("UsoMesaBillar", back_populates="ventas")
    metodo_pago = relationship("MetodoPago", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta")


class DetalleVenta(Base):
    __tablename__ = 'DetalleVenta'
    id_venta = Column(Integer, ForeignKey('Venta.id_venta'), primary_key=True)
    id_producto = Column(Integer, ForeignKey('Producto.id_producto'), primary_key=True)
    cantidad = Column(Integer)
    precio_unitario = Column(DECIMAL(14, 2))
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")


class HorarioEmpleado(Base):
    __tablename__ = 'HorarioEmpleado'
    id_empleado = Column(Integer, ForeignKey('Empleado.id_empleado'), primary_key=True)
    id_turno = Column(Integer, ForeignKey('Turno.id_turno'), primary_key=True)
    fecha = Column(Date)
    empleado = relationship("Empleado", back_populates="horarios")
    turno = relationship("Turno", back_populates="empleados")
