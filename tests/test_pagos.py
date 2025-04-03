import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.testing import fixture
from sqlmodel import Session

from ..models import Pago, Paciente, Direccion, Colonia, Estado, FormaPago, CondicionPago

@pytest.fixture
def setup(session: Session, client: TestClient):
    estado = Estado(nombre="CDMX")
    session.add(estado)
    session.commit()

    colonia = Colonia(codigo_postal="09660", nombre="Citlalli", municipio="Iztapalapa", ciudad="CDMX",
                      estado_id=estado.id)
    session.add(colonia)
    session.commit()

    direccion = Direccion(calle="Antonio", num_exterior="9", colonia_id=colonia.id)
    session.add(direccion)
    session.commit()

    formaPago = FormaPago(nombre="Tarjeta débito")
    session.add(formaPago)
    session.commit()

    condicionPago = CondicionPago(nombre="En visita")
    session.add(condicionPago)
    session.commit()

    paciente = Paciente(nombre="Pepito", fecha_nacimiento=datetime.datetime.now(), edad=24, numero_paciente="0001",
                        direccion_id=1)
    session.add(paciente)
    session.commit()




def test_se_valida_que_el_monto_pagado_no_supere_el_monto_de_la_venta(setup, session: Session, client: TestClient):
    pass


def test_se_valida_que_el_monto_pagado_no_sea_menor_que_el_monto_de_la_venta(setup, session: Session, client: TestClient):
    pass

def test_se_valida_que_el_pago_sea_diferido_en_varios_pagos_si_tiene_credito_el_cliente(setup, session: Session, client: TestClient):
    pass