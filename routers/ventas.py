from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select
from starlette import status

from ..database import SessionDep
from ..models import Venta, VentaBase, VentaPublic, VentaCreate, ItemVenta, VentaUpdate

router = APIRouter(
    prefix='/ventas',
    tags=['ventas']
)


@router.get('/', response_model=list[VentaPublic], status_code=status.HTTP_200_OK)
async def read_ventas(session: SessionDep):
    statement = select(Venta).where(Venta.deleted_at == None)
    results = session.exec(statement).all()
    return results

@router.get('/{venta_id}')
async def busqueda(session: SessionDep, venta_id: int):
    venta_id = session.query(Venta).where(Venta.deleted_at == None).filter(Venta.id == venta_id).first()
    if venta_id is not None:
        return venta_id
    raise HTTPException(status_code=404, detail='Venta no encontrada')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_venta(session: SessionDep, venta_request: VentaCreate):
    costo_total = sum(item.costo for item in venta_request.items)
    venta_data = venta_request.model_dump()
    venta_data['costo'] = costo_total
    venta = Venta.model_validate(venta_data)
    session.add(venta)
    session.commit()
    for i in venta_request.items:
        i.venta_id = venta.id
        item = ItemVenta.model_validate(i)
        session.add(item)
        session.commit()


@router.put('/update/{id}', status_code=status.HTTP_201_CREATED)
async def update_venta(session: SessionDep, venta_request: VentaUpdate, id: int = Path(gt=0)):
    venta = session.get(Venta, id)
    if venta is not None:
        venta_data = venta_request.model_dump()
        venta.updated_at = datetime.now()
        venta.sqlmodel_update(venta_data)
        session.add(venta)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se pudo actualizar la venta')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restor_venta(session: SessionDep, id: int = Path(gt=0)):
    venta = session.get(Venta, id)
    if venta is not None:
        venta.deleted_at = None
        session.add(venta)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se pudo reestablecer la venta')



@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_venta(session: SessionDep, id: int = Path(gt=0)):
    venta = session.get(Venta, id)
    if venta is not None:
        venta.deleted_at = datetime.now()
        session.add(venta)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se puede eliminar la venta')
