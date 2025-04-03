from decimal import Decimal

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None

class RolBase(SQLModel):
    nombre: str = Field(unique=True)


class RolPublic(RolBase):
    id: int


class Rol(RolBase, table=True):
    __tablename__ = 'roles'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)
    usuarios: list['Usuario'] = Relationship(back_populates='rol')


class UsuarioBase(SQLModel):
    nombre_completo: str = Field(min_length=3, max_length=255)
    correo: str = Field(EmailStr, unique=True)
    telefono: str | None = None
    rol_id: int = Field(foreign_key='roles.id')

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioPublic(UsuarioBase):
    id: int


class Usuario(UsuarioBase, table=True):
    __tablename__ = 'usuarios'
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str | None = Field(default=None)
    rol_id: int = Field(foreign_key='roles.id')
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)


    rol: Rol = Relationship(back_populates='usuarios')
    pacientes: list['Paciente'] = Relationship(back_populates='usuario')


class EstadoBase(SQLModel):
    nombre: str


class EstadoPublic(EstadoBase):
    id: int


class Estado(EstadoBase, table=True):
    __tablename__ = 'estados'
    id: int | None = Field(default=None, primary_key=True)

    colonias: list['Colonia'] = Relationship(back_populates='estado')


class ColoniaBase(SQLModel):
    codigo_postal: str
    nombre: str
    municipio: str
    ciudad: str
    estado_id: int = Field(foreign_key='estados.id')


class ColoniaPublic(ColoniaBase):
    id: int


class Colonia(ColoniaBase, table=True):
    __tablename__ = 'colonias'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    estado: Estado = Relationship(back_populates='colonias')
    direcciones: list['Direccion'] = Relationship(back_populates='colonia')


class DireccionBase(SQLModel):
    calle: str
    num_extrerior: str
    num_interior: str | None
    colonia_id: int = Field(foreign_key='colonias.id')


class DireccionPublic(DireccionBase):
    id: int
    colonia: ColoniaPublic


class Direccion(DireccionBase, table=True):
    __tablename__ = 'direcciones'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    colonia: Colonia = Relationship(back_populates='direcciones')
    sucursales: list['Sucursal'] = Relationship(back_populates='direccion')
    empleados: list['Empleado'] = Relationship(back_populates='direccion')
    pacientes: list['Paciente'] = Relationship(back_populates='direccion')


class SucursalBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=255)
    telefono: str | None


class SucursalPublic(SucursalBase):
    id: int
    direccion: DireccionPublic | None


class SucursalCreate(SucursalBase):
    direccion: DireccionBase


class SucursalUpdate(SucursalBase):
    direccion: DireccionBase


class Sucursal(SucursalBase, table=True):
    __tablename__ = 'sucursales'
    id: int | None = Field(default=None, primary_key=True)
    direccion_id: int = Field(foreign_key='direcciones.id')
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    direccion: Direccion = Relationship(back_populates='sucursales')
    empleados: list['Empleado'] = Relationship(back_populates='sucursal')


class DepartamentoEmpleado(SQLModel, table=True):
    __tablename__ = 'departamento_empleado'
    id: int | None = Field(default=None, primary_key=True)
    empleado_id: int = Field(foreign_key='empleados.id', primary_key=True)
    departamento_id: int = Field(foreign_key='departamentos.id', primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)


class EmpleadoBase(SQLModel):
    nombre_completo: str = Field(min_length=3, max_length=255)
    fecha_nacimiento: date
    telefono: str = Field(max_length=15)
    correo: str = Field(unique=True)
    sucursal_id: int = Field(foreign_key='sucursales.id', gt=0)


class EmpleadoPublic(EmpleadoBase):
    id: int
    direccion: DireccionPublic
    sucursal: SucursalBase


class EmpleadoCreate(EmpleadoBase):
    direccion: DireccionBase


class EmpleadoUpdate(EmpleadoBase):
    direccion: DireccionBase


class Empleado(EmpleadoBase, table=True):
    __tablename__ = 'empleados'
    id: int | None = Field(default=None, primary_key=True)
    direccion_id: int = Field(foreign_key='direcciones.id')
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    direccion: Direccion = Relationship(back_populates='empleados')
    sucursal: Sucursal = Relationship(back_populates='empleados')
    cotizacion: list['Cotizacion'] = Relationship(back_populates='empleado')
    resultados: list['Resultado'] = Relationship(back_populates='empleado')
    ventas: list['Venta'] = Relationship(back_populates='empleado')
    departamentos: list['Departamento'] = Relationship(back_populates='empleados', link_model=DepartamentoEmpleado)


class DepartamentoBase(SQLModel):
    nombre: str = Field(min_length=3)


class DepartamentoPublic(DepartamentoBase):
    id: int


class Departamento(DepartamentoBase, table=True):
    __tablename__ = 'departamentos'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    empleados: list['Empleado'] = Relationship(back_populates='departamentos', link_model=DepartamentoEmpleado)


class PacienteBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=128)
    fecha_nacimiento: date
    edad: int = Field(default=0)
    numero_paciente: str


class PacientePublic(PacienteBase):
    id: int


class PacienteCreate(PacienteBase):
    direccion: DireccionBase


class PacienteUpdate(PacienteBase):
    direccion: DireccionBase


class Paciente(PacienteBase, table=True):
    __tablename__ = 'pacientes'
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int | None = Field(default=None, foreign_key='usuarios.id')
    direccion_id: int = Field(foreign_key='direcciones.id')
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    direccion: Direccion = Relationship(back_populates='pacientes')
    usuario: Usuario | None = Relationship(back_populates='pacientes')
    cotizacion: list['Cotizacion'] = Relationship(back_populates='paciente')
    citas: list['Cita'] = Relationship(back_populates='paciente')


class FormaPagoBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=128)


class FormaPagoPublic(FormaPagoBase):
    id: int


class FormaPago(FormaPagoBase, table=True):
    __tablename__ = 'formas_pagos'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    cotizacion: list['Cotizacion'] = Relationship(back_populates='formapago')
    pago: list['Pago'] = Relationship(back_populates='formapago')


class CondicionPagoBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=128)


class CondicionPagoPublic(CondicionPagoBase):
    id: int


class CondicionPago(CondicionPagoBase, table=True):
    __tablename__ = 'condiciones_pagos'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    cotizacion: list['Cotizacion'] = Relationship(back_populates='condicion')
    pago: list['Pago'] = Relationship(back_populates='condicion')


class CategoriaBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=128)


class CategoriaPublic(CategoriaBase):
    id: int


class Categoria(CategoriaBase, table=True):
    __tablename__ = 'categorias'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    productoservicio: list['ProductoServicio'] = Relationship(back_populates='categoria')


class ProductoBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=128)
    descripcion: str
    tipo_muestra: str
    precio_compra: Decimal = Field(max_digits=9, decimal_places=2)
    precio_venta: Decimal = Field(max_digits=9, decimal_places=2)
    tiempo_entrega: int
    codigo: str | None
    volumen: str | None
    presentacion: str | None
    conservacion: str | None
    contenido: str | None
    utilidad: str | None
    categoria_id: int = Field(foreign_key='categorias.id')


class ProductoPublic(ProductoBase):
    id: int


class ProductoServicio(ProductoBase, table=True):
    __tablename__ = 'productos_servicios'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    categoria: Categoria = Relationship(back_populates='productoservicio')
    itemsVenta: list['ItemVenta'] = Relationship(back_populates='productoservicio')
    itemcotizacion: list['ItemCotizacion'] = Relationship(back_populates='productoservicio')


class ItemCotizacionBase(SQLModel):
    costo: Decimal = Field(max_digits=9, decimal_places=2)
    producto_servicio_id: int = Field(foreign_key='productos_servicios.id')
    cotizacion_id: int | None = Field(default=None)


class CotizacionBase(SQLModel):
    fecha_elaboracion: date
    tratamiento: str | None
    empleado_id: int = Field(foreign_key='empleados.id')
    paciente_id: int = Field(foreign_key='pacientes.id')
    forma_pago_id: int = Field(foreign_key='formas_pagos.id')
    condiciones_pago_id: int = Field(foreign_key='condiciones_pagos.id')


class CotizacionCreate(CotizacionBase):
    items: list[ItemCotizacionBase]


class CotizacionUpdate(CotizacionBase):
    items: list[ItemCotizacionBase]


class CotizacionPublic(CotizacionBase):
    id: int
    costo: Decimal
    paciente: PacientePublic
    empleado: EmpleadoPublic
    formapago: FormaPagoPublic
    condicion: CondicionPagoPublic


class Cotizacion(CotizacionBase, table=True):
    __tablename__ = 'cotizaciones'
    id: int | None = Field(default=None, primary_key=True)
    costo: Decimal = Field(max_digits=9, decimal_places=2)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    empleado: Empleado = Relationship(back_populates='cotizacion')
    paciente: Paciente = Relationship(back_populates='cotizacion')
    formapago: FormaPago = Relationship(back_populates='cotizacion')
    condicion: CondicionPago = Relationship(back_populates='cotizacion')
    citas: list['Cita'] = Relationship(back_populates='cotizacion')
    itemcotizacion: list['ItemCotizacion'] = Relationship(back_populates='cotizacion')


class ItemCotizacion(ItemCotizacionBase, table=True):
    __tablename__ = 'item_cotizaciones'
    id: int | None = Field(default=None, primary_key=True)
    cotizacion_id: int = Field(foreign_key='cotizaciones.id')
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    productoservicio: ProductoServicio = Relationship(back_populates='itemcotizacion')
    cotizacion: Cotizacion = Relationship(back_populates='itemcotizacion')


class CitaBase(SQLModel):
    fecha: datetime
    fecha_confirmacion: datetime
    paciente_id: int = Field(foreign_key='pacientes.id')
    cotizacion_id: int = Field(foreign_key='cotizaciones.id')



class CitaPublic(CitaBase):
    id: int
    paciente: PacientePublic
    cotizacion: CotizacionPublic


class Cita(CitaBase, table=True):
    __tablename__ = 'citas'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    paciente: Paciente = Relationship(back_populates='citas')
    cotizacion: Cotizacion = Relationship(back_populates='citas')
    resultado: list['Resultado'] = Relationship(back_populates='cita')
    venta: list['Venta'] = Relationship(back_populates='cita')


class ResultadoBase(SQLModel):
    documentos_url: str = Field(min_length=3, max_length=255)
    observaciones: str = Field(min_length=3, max_length=255)
    cita_id: int = Field(foreign_key='citas.id')
    empleado_id: int = Field(foreign_key='empleados.id')


class ResultadoPublic(ResultadoBase):
    id: int


class Resultado(ResultadoBase, table=True):
    __tablename__ = 'resultados'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    cita: Cita = Relationship(back_populates='resultado')
    empleado: Empleado = Relationship(back_populates='resultados')


class ItemVentaBase(SQLModel):
    costo: Decimal = Field(max_digits=9, decimal_places=2)
    cantidad: Decimal = Field(max_digits=9, decimal_places=2)
    venta_id: int = Field(foreign_key='ventas.id')
    producto_servicio_id: int = Field(foreign_key='productos_servicios.id')


class VentaBase(SQLModel):
    costo: Decimal = Field(max_digits=9, decimal_places=2)
    fecha: datetime
    cita_id: int = Field(foreign_key='citas.id')
    empleado_id: int = Field(foreign_key='empleados.id')


class VentaCreate(VentaBase):
    items: list[ItemVentaBase]


class VentaUpdate(VentaBase):
    items: list[ItemVentaBase]


class VentaPublic(VentaBase):
    id: int


class Venta(VentaBase, table=True):
    __tablename__ = 'ventas'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    cita: Cita = Relationship(back_populates='venta')
    empleado: Empleado = Relationship(back_populates='ventas')
    itemsVenta: list['ItemVenta'] = Relationship(back_populates='venta')
    pago: list['Pago'] = Relationship(back_populates='venta')


class ItemVenta(ItemVentaBase, table=True):
    __tablename__ = 'items_ventas'
    id: int | None = Field(default=None, primary_key=True)
    venta_id: int = Field(foreign_key='ventas.id')
    producto_servicio_id: int = Field(foreign_key='productos_servicios.id')
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    venta: Venta = Relationship(back_populates='itemsVenta')
    productoservicio: ProductoServicio = Relationship(back_populates='itemsVenta')


class PagoBase(SQLModel):
    fecha: date
    monto: Decimal = Field(max_digits=9, decimal_places=2)
    referencia: str = Field(min_length=3, max_length=255)
    forma_pago_id: int = Field(foreign_key='formas_pagos.id')
    condicion_pago_id: int = Field(foreign_key='condiciones_pagos.id')
    venta_id: int = Field(foreign_key='ventas.id')


class PagoPublic(PagoBase):
    id: int
    condicion: CondicionPagoPublic
    formapago: FormaPagoPublic
    venta: VentaPublic


class Pago(PagoBase, table=True):
    __tablename__ = 'pagos'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

    formapago: FormaPago = Relationship(back_populates='pago')
    condicion: CondicionPago = Relationship(back_populates='pago')
    venta: Venta = Relationship(back_populates='pago')


class ContactoBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=128)
    apellidos: str = Field(min_length=3, max_length=128)
    telefono: str = Field(max_length=15)
    correo: str = Field(unique=True)
    comentario: str = Field(min_length=20)
    receta_url: str | None = Field(default=None)


class ContactoPublic(ContactoBase):
    id: int


class Contacto(ContactoBase, table=True):
    __tablename__ = 'contactos'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)

class QuejaBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=200)
    correo: str = Field(max_length=200)
    observacion: str

class QuejaPublic(QuejaBase):
    id: int

class Queja(QuejaBase, table=True):
    __tablename__ = 'quejas'
    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    deleted_at: datetime | None = Field(default=None)
