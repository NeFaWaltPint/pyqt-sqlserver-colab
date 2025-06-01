from sqlalchemy import Column, Integer, String, Date, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Tabla: Turno
class Turno(Base):
    __tablename__ = 'Turno'
    id_turno = Column(Integer, primary_key=True, nullable=False)
    nombre_turno = Column(String(100))
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)

    horarios = relationship('HorarioEmpleado', back_populates='turno')


# Tabla: MetodoPago
class MetodoPago(Base):
    __tablename__ = 'MetodoPago'
    id_metodo_pago = Column(Integer, primary_key=True, nullable=False)
    descripcion = Column(String(100))

    ventas = relationship('Venta', back_populates='metodo_pago')


# Tabla: Empleado
class Empleado(Base):
    __tablename__ = 'Empleado'
    id_empleado = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(String(100))
    apellido = Column(String(100))
    salario = Column(DECIMAL(10, 2))
    fecha_ingreso = Column(Date)

    mesas_asignadas = relationship('MesaBillar', back_populates='empleado')
    ventas = relationship('Venta', back_populates='empleado')
    horarios = relationship('HorarioEmpleado', back_populates='empleado')
    mesas = relationship('EmpleadoMesa', back_populates='empleado')


# Tabla: MesaBillar
class MesaBillar(Base):
    __tablename__ = 'MesaBillar'
    id_mesa = Column(Integer, primary_key=True, nullable=False)
    id_empleado = Column(Integer, ForeignKey('Empleado.id_empleado'))
    estado = Column(String(50))

    # relación directa
    empleado = relationship('Empleado', back_populates='mesas_asignadas')
    
    # relación inversa
    juegos = relationship('Juego', back_populates='mesa')
    ventas = relationship('Venta', back_populates='mesa')
    empleados = relationship('EmpleadoMesa', back_populates='mesa')


# Tabla: Juego
class Juego(Base):
    __tablename__ = 'Juego'
    id_juego = Column(Integer, primary_key=True, nullable=False)
    id_mesa = Column(Integer, ForeignKey('MesaBillar.id_mesa'))
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    total_juegos = Column(DECIMAL(10, 2))

    # relación directa
    mesa = relationship('MesaBillar', back_populates='juegos')


# Tabla: EmpleadoMesa
class EmpleadoMesa(Base):
    __tablename__ = 'EmpleadoMesa'
    id_empleado = Column(Integer, ForeignKey('Empleado.id_empleado'), primary_key=True)
    id_mesa = Column(Integer, ForeignKey('MesaBillar.id_mesa'), primary_key=True)

    # relación directa
    empleado = relationship('Empleado', back_populates='mesas')
    mesa = relationship('MesaBillar', back_populates='empleados')


# Tabla: HorarioEmpleado
class HorarioEmpleado(Base):
    __tablename__ = 'HorarioEmpleado'
    id_empleado = Column(Integer, ForeignKey('Empleado.id_empleado'), primary_key=True)
    id_turno = Column(Integer, ForeignKey('Turno.id_turno'), primary_key=True)

    # relación directa
    empleado = relationship('Empleado', back_populates='horarios')
    turno = relationship('Turno', back_populates='horarios')


# Tabla: Producto
class Producto(Base):
    __tablename__ = 'Producto'
    id_producto = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(String(50))
    categoria = Column(String(50))
    unidad_medida = Column(String(50))
    precio_compra = Column(DECIMAL(14, 2))
    precio_venta = Column(DECIMAL(14, 2))
    cantidad_stock = Column(Integer)

    # relación inversa
    detalle_ventas = relationship('DetalleVenta', back_populates='producto')
    detalle_compras = relationship('DetalleCompra', back_populates='producto')


# Tabla: Venta
class Venta(Base):
    __tablename__ = 'Venta'
    id_venta = Column(Integer, primary_key=True, nullable=False)
    total_venta = Column(DECIMAL(14, 2))
    fecha = Column(DateTime)
    id_empleado = Column(Integer, ForeignKey('Empleado.id_empleado'))
    id_mesa = Column(Integer, ForeignKey('MesaBillar.id_mesa'))
    id_metodo_pago = Column(Integer, ForeignKey('MetodoPago.id_metodo_pago'))

    empleado = relationship('Empleado', back_populates='ventas')
    mesa = relationship('MesaBillar', back_populates='ventas')
    metodo_pago = relationship('MetodoPago', back_populates='ventas')

    # relación inversa
    detalles = relationship('DetalleVenta', back_populates='venta')


# Tabla: DetalleVenta
class DetalleVenta(Base):
    __tablename__ = 'DetalleVenta'
    id_venta = Column(Integer, ForeignKey('Venta.id_venta'), primary_key=True)
    id_producto = Column(Integer, ForeignKey('Producto.id_producto'), primary_key=True)
    cantidad = Column(Integer)
    precio_unitario = Column(DECIMAL(14, 2))

    # relación inversa
    venta = relationship('Venta', back_populates='detalles')
    producto = relationship('Producto', back_populates='detalle_ventas')


# Tabla: Proveedor
class Proveedor(Base):
    __tablename__ = 'Proveedor'
    id_proveedor = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(String(100))
    telefono = Column(String(20))
    correo = Column(String(100))
    direccion = Column(String(200))

    # relación inversa
    compras = relationship('Compra', back_populates='proveedor')


# Tabla: Compra
class Compra(Base):
    __tablename__ = 'Compra'
    id_compra = Column(Integer, primary_key=True, nullable=False)
    id_proveedor = Column(Integer, ForeignKey('Proveedor.id_proveedor'))
    total_compra = Column(DECIMAL(14, 2))
    fecha = Column(DateTime)

    # relación directa
    proveedor = relationship('Proveedor', back_populates='compras')
    
    # relación inversa
    detalles = relationship('DetalleCompra', back_populates='compra')


# Tabla: DetalleCompra
class DetalleCompra(Base):
    __tablename__ = 'DetalleCompra'
    id_compra = Column(Integer, ForeignKey('Compra.id_compra'), primary_key=True)
    id_producto = Column(Integer, ForeignKey('Producto.id_producto'), primary_key=True)
    cantidad = Column(Integer)
    precio_unitario = Column(DECIMAL(14, 2))

    # relación directa
    compra = relationship('Compra', back_populates='detalles')
    producto = relationship('Producto', back_populates='detalle_compras')
