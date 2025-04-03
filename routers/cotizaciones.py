from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select
from starlette import status

from ..database import SessionDep
from ..models import Cotizacion, CotizacionPublic, CotizacionCreate, ItemCotizacion, CotizacionUpdate

router = APIRouter(
    prefix='/cotizaciones',
    tags=['cotizaciones']
)


@router.get('/', response_model=list[CotizacionPublic], status_code=status.HTTP_200_OK)
async def read_cotizaciones(session: SessionDep):
    statement = select(Cotizacion).where(Cotizacion.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{cotizacion_id}')
async def busqueda(session: SessionDep, cotizacion_id: int):
    cotizacion_id = session.query(Cotizacion).where(Cotizacion.deleted_at == None).filter(Cotizacion.id == cotizacion_id).first()
    if cotizacion_id is not None:
        return cotizacion_id
    raise HTTPException(status_code=404, detail='Cotización no encontrada')


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_cotizacion(session: SessionDep, cotizacion_request: CotizacionCreate):
    costo_total = sum(item.costo for item in cotizacion_request.items)

    cotizacion_data = cotizacion_request.model_dump()
    cotizacion_data['costo'] = costo_total
    cotizacion = Cotizacion.model_validate(cotizacion_data)
    session.add(cotizacion)
    session.commit()
    for i in cotizacion_request.items:
        i.cotizacion_id = cotizacion.id
        item = ItemCotizacion.model_validate(i)
        session.add(item)
        session.commit()


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_cotizacion(session: SessionDep, cotizacion_request: CotizacionUpdate, id: int = Path(gt=0)):
    cotizacion = session.get(Cotizacion, id)
    if cotizacion is not None:
        cotizacion_data = cotizacion_request.model_dump()
        cotizacion.updated_at = datetime.now()
        cotizacion.sqlmodel_update(cotizacion_data)
        session.add(cotizacion)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='La cotizacion no pudo ser actualizada')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restor_cotizacion(session: SessionDep, id: int = Path(gt=0)):
    cotizacion = session.get(Cotizacion, id)
    if cotizacion is not None:
        cotizacion.deleted_at = None
        session.add(cotizacion)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se pudo reestablecer la cotizacion')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cotizacion(session: SessionDep, id: int = Path(gt=0)):
    cotizacion = session.get(Cotizacion, id)
    if cotizacion is not None:
        cotizacion.deleted_at = datetime.now()
        session.add(cotizacion)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se puede eliminar la cotizacion')
