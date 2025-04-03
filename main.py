from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import categorias, productos, contactos, departamentos, roles, empleados, estados, colonias, sucursales, \
    pacientes, condicion_pago, forma_pago, cotizaciones, citas, ventas, pagos, resultados, usuarios, quejas, auth

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(productos.router)
app.include_router(contactos.router)
app.include_router(departamentos.router)
app.include_router(roles.router)
app.include_router(empleados.router)
app.include_router(estados.router)
app.include_router(colonias.router)
app.include_router(sucursales.router)
app.include_router(pacientes.router)
app.include_router(condicion_pago.router)
app.include_router(forma_pago.router)
app.include_router(cotizaciones.router)
app.include_router(citas.router)
app.include_router(ventas.router)
app.include_router(pagos.router)
app.include_router(resultados.router)
app.include_router(usuarios.router)
app.include_router(quejas.router)
