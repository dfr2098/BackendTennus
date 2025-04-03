from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from starlette import status
from sqlmodel import select

from ..models import CondicionPagoBase, CondicionPago, CondicionPagoPublic
from ..database import SessionDep

router = APIRouter(
    prefix='/condicion_pago',
    tags=['condicion de pago']
)


@router.get('/', response_model=list[CondicionPagoPublic], status_code=status.HTTP_200_OK)
async def read_condicon_pago(session: SessionDep):
    statement = select(CondicionPago).where(CondicionPago.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{condicion_pago_id}')
async def busqueda(session: SessionDep, condicion_pago_id: int):
    condicion_pago_id = session.query(CondicionPago).where(CondicionPago.deleted_at == None).filter(CondicionPago.id == condicion_pago_id).first()
    if condicion_pago_id is not None:
        return condicion_pago_id
    raise HTTPException(status_code=404, detail='Condicion de pago no encontrada')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_condicion_pago(session: SessionDep, condicion_request: CondicionPagoBase):
    condicion = CondicionPago.model_validate(condicion_request)
    session.add(condicion)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_condicion(session: SessionDep, condicion_request: CondicionPagoBase, id: int = Path(gt=0)):
    condicion = session.get(CondicionPago, id)
    if condicion is not None:
        condicion_data = condicion_request.model_dump(exclude_unset=True)
        condicion.updated_at = datetime.now()
        condicion.sqlmodel_update(condicion_data)
        session.add(condicion)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se encontro la condicion de pago')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_condicion(session: SessionDep, id: int = Path(gt=0)):
    condicion = session.get(CondicionPago, id)
    if condicion is not None:
        condicion.deleted_at = None
        session.add(condicion)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Condicion de pago no encontrada')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_condicion(session: SessionDep, id: int = Path(gt=0)):
    condicion = session.get(CondicionPago, id)
    print(condicion)
    if condicion is not None:
        condicion.deleted_at = datetime.now()
        session.add(condicion)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Condicion de pago no encontrada')
