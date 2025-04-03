from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from starlette import status
from sqlmodel import select

from ..models import PacienteBase, PacientePublic, Paciente, Direccion, PacienteUpdate, PacienteCreate
from ..database import SessionDep

router = APIRouter(
    prefix='/pacientes',
    tags=['pacientes']
)

@router.get('/', response_model=list[PacientePublic], status_code=status.HTTP_200_OK)
async def read_pacientes(session: SessionDep):
    statement = select(Paciente).where(Paciente.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{paciente_id}')
async def busqueda(session: SessionDep, paciente_id: int):
    paciente_id = session.query(Paciente).where(Paciente.deleted_at == None).filter(Paciente.id == paciente_id).first()
    if paciente_id is not None:
        return paciente_id
    raise HTTPException(status_code=404, detail='Categoria no encontrada')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_paciente(session: SessionDep, paciente_request: PacienteCreate):
    direccion = Direccion.model_validate(paciente_request.direccion)
    session.add(direccion)

    session.commit()

    empleado_data = paciente_request.model_dump(exclude=['direccion'])
    empleado_data['direccion_id'] = direccion.id

    paciente = Paciente.model_validate(empleado_data)
    session.add(paciente)
    session.commit()

@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_paciente(session: SessionDep, paciente_request: PacienteUpdate, id: int = Path(gt=0)):
    paciente = session.get(Paciente, id)
    if paciente is not None:
        paciente_data = paciente_request.model_dump(exclude_unset=True)
        paciente.updated_at = datetime.now()
        paciente.sqlmodel_update(paciente_data)
        session.add(paciente)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se encontro el paciente')

    direccion = session.get(Direccion, paciente.direccion_id)
    if direccion is not None:
        direccion_data = paciente_request.direccion.model_dump(exclude_unset=True)
        direccion.updated_at = datetime.now()
        direccion.sqlmodel_update(direccion_data)
        session.add(direccion)
        session.commit()

@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_paciente(session: SessionDep, id: int = Path(gt=0)):
    paciente = session.get(Paciente, id)
    if paciente is not None:
        paciente.deleted_at = None

        direccion = session.get(Direccion, paciente.direccion_id)
        if direccion is not None:
            direccion.deleted_at = None
            session.add(paciente)
            session.commit()
            session.add(direccion)
            session.commit()
    else:
        raise HTTPException(status_code=404, detail='Paciente no encontrado')

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_paciente(session: SessionDep, id: int = Path(gt=0)):
    paciente = session.get(Paciente, id)
    if paciente is not None:
        paciente.deleted_at = datetime.now()
        direccion = session.get(Direccion, paciente.direccion_id)
        if direccion is not None:
            direccion.deleted_at = datetime.now()
            session.add(paciente)
            session.commit()
            session.add(direccion)
            session.commit()
    else:
        raise HTTPException(status_code=404, detail='Paciente no encontrado')