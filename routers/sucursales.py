from datetime import datetime

from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status
from sqlmodel import select

from ..models import SucursalBase, Sucursal, SucursalPublic, SucursalCreate, Direccion, SucursalUpdate
from ..database import SessionDep

router = APIRouter(
    prefix='/sucursales',
    tags=['sucursales']
)


@router.get('/', response_model=list[SucursalPublic], status_code=status.HTTP_200_OK)
async def read_sucursales(session: SessionDep):
    statement = select(Sucursal).where(Sucursal.deleted_at == None)
    results = session.exec(statement).all()
    print(results)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No se encontro la sucursal')
    return results


@router.get('/{sucursal_id}')
async def busqueda(session: SessionDep, sucursal_id: int):
    sucursal_id = session.query(Sucursal).where(Sucursal.deleted_at == None).filter(Sucursal.id == sucursal_id).first()
    if sucursal_id is not None:
        return sucursal_id
    raise HTTPException(status_code=404, detail='Sucursal no encontrada')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_sucursal(session: SessionDep, sucursal_request: SucursalCreate):
    direccion = Direccion.model_validate(sucursal_request.direccion)
    session.add(direccion)
    session.commit()

    sucursal_data = sucursal_request.model_dump(exclude=['direccion'])
    sucursal_data['direccion_id'] = direccion.id

    sucursal = Sucursal.model_validate(sucursal_data)
    session.add(sucursal)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_sucursal(session: SessionDep, sucursal_request: SucursalUpdate, id: int = Path(gt=0)):
    sucursal = session.get(Sucursal, id)
    if sucursal is not None:
        sucursal_data = sucursal_request.model_dump(exclude_unset=True)
        sucursal.updated_at = datetime.now()
        sucursal.sqlmodel_update(sucursal_data)
        session.add(sucursal)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Sucursal no encontrada')

    direccion = session.get(Direccion, sucursal.direccion_id)
    if direccion is not None:
        direccion_data = sucursal_request.direccion.model_dump(exclude_unset=True)
        direccion.updated_at = datetime.now()
        direccion.sqlmodel_update(direccion_data)
        session.add(direccion)
        session.commit()


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_sucursal(session: SessionDep, id: int = Path(gt=0)):
    sucursal = session.get(Sucursal, id)
    if sucursal is not None:
        sucursal.deleted_at = None

        direccion = session.get(Direccion, sucursal.direccion_id)
        if direccion is not None:
            direccion.deleted_at = None
            session.add(sucursal)
            session.commit()
            session.add(direccion)
            session.commit()

    else:
        raise status.HTTP_404_NOT_FOUND(detail='sucursal no reestablecida')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_sucursal(session: SessionDep, id: int = Path(gt=0)):
    sucursal = session.get(Sucursal, id)
    if sucursal is not None:
        sucursal.deleted_at = datetime.now()
        direccion = session.get(Direccion, sucursal.direccion_id)
        if direccion is not None:
            direccion.deleted_at = datetime.now()
            session.add(sucursal)
            session.commit()
            session.add(direccion)
            session.commit()

    else:
        raise status.HTTP_404_NOT_FOUND(detail='sucursal no eliminada')
