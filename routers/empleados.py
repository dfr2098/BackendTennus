from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from starlette import status
from sqlmodel import select

from ..models import EmpleadoBase, EmpleadoPublic, Empleado, Direccion, EmpleadoCreate, EmpleadoUpdate
from ..database import SessionDep

router = APIRouter(
    prefix='/empleados',
    tags=['empleados']
)


@router.get('/', response_model=list[EmpleadoPublic], status_code=status.HTTP_200_OK)
async def read_empleados(session: SessionDep):
    statement = select(Empleado).where(Empleado.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{empleado_id}')
async def busqueda(session: SessionDep, empleado_id: int):
    empleado_id = session.query(Empleado).where(Empleado.deleted_at == None).filter(Empleado.id == empleado_id).first()
    if empleado_id is not None:
        return empleado_id
    raise HTTPException(status_code=404, detail='Empleado no encontrado')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_empleado(session: SessionDep, empleado_request: EmpleadoCreate):
    direccion = Direccion.model_validate(empleado_request.direccion)
    session.add(direccion)
    session.commit()

    empleado_data = empleado_request.model_dump(exclude=['direccion'])
    empleado_data['direccion_id'] = direccion.id

    empleado = Empleado.model_validate(empleado_data)
    session.add(empleado)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_empleado(session: SessionDep, empleado_request: EmpleadoUpdate, id: int = Path(gt=0)):
    empleado = session.get(Empleado, id)
    if empleado is not None:
        empleado_data = empleado_request.model_dump(exclude_unset=True)
        empleado.updated_at = datetime.now()
        empleado.sqlmodel_update(empleado_data)
        session.add(empleado)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se encontro el empleado')

    direccion = session.get(Direccion, empleado.direccion_id)
    if direccion is not None:
        direccion_data = empleado_request.direccion.model_dump(exclude_unset=True)
        direccion.updated_at = datetime.now()
        direccion.sqlmodel_update(direccion_data)
        session.add(direccion)
        session.commit()


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_empleado(session: SessionDep, id: int = Path(gt=0)):
    empleado = session.get(Empleado, id)
    if empleado is not None:
        empleado.deleted_at = None

        direccion = session.get(Direccion, empleado.direccion_id)
        if direccion is not None:
            direccion.deleted_at = None
            session.add(empleado)
            session.commit()
            session.add(direccion)
            session.commit()
    else:
        raise HTTPException(status_code=404, detail='Empleado no encontrado')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_empleado(session: SessionDep, id: int = Path(gt=0)):
    empleado = session.get(Empleado, id)
    if empleado is not None:
        empleado.deleted_at = datetime.now()
        direccion = session.get(Direccion, empleado.direccion_id)
        if direccion is not None:
            direccion.deleted_at = datetime.now()
            session.add(empleado)
            session.commit()
            session.add(direccion)
            session.commit()
    else:
        raise HTTPException(status_code=404, detail='Empleado no encontrado')
