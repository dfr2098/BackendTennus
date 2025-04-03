from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select
from starlette import status

from ..database import SessionDep
from ..models import Pago, PagoBase, PagoPublic

router = APIRouter(
    prefix='/pagos',
    tags=['pagos']
)


@router.get('/', response_model=list[PagoPublic], status_code=status.HTTP_200_OK)
async def read_pagos(session: SessionDep):
    statement = select(Pago).where(Pago.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{pago_id}')
async def busqueda(session: SessionDep, pago_id: int):
    pago_id = session.query(Pago).where(Pago.deleted_at == None).filter(Pago.id == pago_id).first()
    if pago_id is not None:
        return pago_id
    raise HTTPException(status_code=404, detail='Pago no encontrado')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_pago(session: SessionDep, pago_request: PagoBase):
    pago = Pago.model_validate(pago_request)
    print(pago)
    session.add(pago)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_201_CREATED)
async def update_pago(session: SessionDep, pago_request: PagoBase, id: int = Path(gt=0)):
    pago = session.get(Pago, id)
    if pago is not None:
        pago_data = pago_request.model_dump(exclude_unset=True)
        pago.updated_at = datetime.now()
        pago.sqlmodel_update(pago_data)
        session.add(pago)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se pudo actualizar el pago')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restor_pago(session: SessionDep, id: int = Path(gt=0)):
    pago = session.get(Pago, id)
    if pago is not None:
        pago.deleted_at = None
        session.add(pago)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se pudo reestablecer el pago')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pago(session: SessionDep, id: int = Path(gt=0)):
    pago = session.get(Pago, id)
    if pago is not None:
        pago.deleted_at = datetime.now()
        session.add(pago)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se puede eliminar el pago')
