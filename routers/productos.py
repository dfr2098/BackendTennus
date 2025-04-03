from datetime import datetime

from fastapi import APIRouter, Path, HTTPException
from sqlmodel import select
from starlette import status

from ..models import ProductoServicio, ProductoBase, ProductoPublic
from ..database import SessionDep

router = APIRouter(
    prefix='/productos',
    tags=['productos']
)


@router.get('/', response_model=list[ProductoPublic], status_code=status.HTTP_200_OK)
async def read_productos(session: SessionDep):
    statement = select(ProductoServicio).where(ProductoServicio.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{producto_id}')
async def busqueda(session: SessionDep, producto_id: int):
    producto_id = session.query(ProductoServicio).where(ProductoServicio.deleted_at == None).filter(ProductoServicio.id == producto_id).first()
    if producto_id is not None:
        return producto_id
    raise HTTPException(status_code=404, detail='Producto o servicio no encontrado')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_producto(session: SessionDep, producto_request: ProductoBase):
    producto = ProductoServicio.model_validate(producto_request)
    session.add(producto)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_producto(session: SessionDep, producto_request: ProductoBase, id: int = Path(gt=0)):
    producto = session.get(ProductoServicio, id)
    if producto is not None:
        producto_data = producto_request.model_dump(exclude_unset=True)
        producto.updated_at = datetime.now()
        producto.sqlmodel_update(producto_data)
        session.add(producto)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Producto no encontrado')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_producto(session: SessionDep, id: int = Path(gt=0)):
    producto = session.get(ProductoServicio, id)
    if producto is not None:
        producto.deleted_at = None
        session.add(producto)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Producto no encontrada')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto(session: SessionDep, id: int = Path(gt=0)):
    producto = session.get(ProductoServicio, id)
    print(producto)
    if producto is not None:
        producto.deleted_at = datetime.now()
        session.add(producto)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Producto no encontrada')
