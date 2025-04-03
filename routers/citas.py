from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select
from starlette import status

from ..database import SessionDep
from ..models import CitaPublic, CitaBase, Cita

router = APIRouter(
    prefix='/citas',
    tags=['citas']
)


@router.get('/', response_model=list[CitaPublic], status_code=status.HTTP_200_OK)
async def read_citas(session: SessionDep):
    statement = select(Cita).where(Cita.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{cita_id}')
async def busqueda(session: SessionDep, cita_id: int):
    cita_id = session.query(Cita).where(Cita.deleted_at == None).filter(Cita.id == cita_id).first()
    if cita_id is not None:
        return cita_id
    raise HTTPException(status_code=404, detail='Cita no encontrada')


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_cita(session: SessionDep, cita_request: CitaBase):
    cita = Cita.model_validate(cita_request)
    session.add(cita)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_201_CREATED)
async def update_cita(session: SessionDep, cita_request: CitaBase, id: int = Path(gt=0)):
    cita = session.get(Cita, id)
    if cita is not None:
        cita_data = cita_request.model_dump(exclude_unset=True)
        cita.updated_at = datetime.now()
        cita.sqlmodel_update(cita_data)
        session.add(cita)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se pudo actualizar la cita')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restor_cita(session: SessionDep, id: int = Path(gt=0)):
    cita = session.get(Cita, id)
    if cita is not None:
        cita.deleted_at = None
        session.add(cita)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se pudo reestablecer la cita')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cita(session: SessionDep, id: int = Path(gt=0)):
    cita = session.get(Cita, id)
    if cita is not None:
        cita.deleted_at = datetime.now()
        session.add(cita)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se puede eliminar la cita')
