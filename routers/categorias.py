from datetime import datetime

from fastapi import APIRouter, Path, HTTPException
from sqlmodel import select
from starlette import status

from ..models import Categoria, CategoriaBase, CategoriaPublic
from ..database import SessionDep
from .auth import AuthDependency

router = APIRouter(
    prefix='/categorias',
    tags=['categorias']
)


@router.get('/', response_model=list[CategoriaPublic], status_code=status.HTTP_200_OK)
async def read_categorias(session: SessionDep):
    statement = select(Categoria).where(Categoria.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{categoria_id}')
async def busqueda(session: SessionDep, categoria_id: int):
    categoria_id = session.query(Categoria).where(Categoria.deleted_at == None).filter(Categoria.id == categoria_id).first()
    if categoria_id is not None:
        return categoria_id
    raise HTTPException(status_code=404, detail='Categoria no encontrada')


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=CategoriaPublic)
async def create_categoria(session: SessionDep, categoria_request: CategoriaBase):
    '''if auth.rol_id != 1:
        raise HTTPException(403, detail='No tiene permisos suficientes') '''
    categoria = Categoria.model_validate(categoria_request)
    session.add(categoria)
    session.commit()

    return categoria


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_categoria(session: SessionDep, categoria_request: CategoriaBase,
                           id: int = Path(gt=0)):
    #if auth.rol_id != 1:
       # raise HTTPException(403, detail='No tiene permisos suficientes')
    categoria = session.get(Categoria, id)
    if categoria is not None:
        categoria_data = categoria_request.model_dump(exclude_unset=True)
        categoria.updated_at = datetime.now()
        categoria.sqlmodel_update(categoria_data)
        session.add(categoria)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Categoria no actualizada')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_categoria(session: SessionDep, auth: AuthDependency, id: int = Path(gt=0)):
    if auth.rol_id != 1:
        raise HTTPException(403, detail='No tiene permisos suficientes')
    categoria = session.get(Categoria, id)
    if categoria is not None:
        categoria.deleted_at = None
        session.add(categoria)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Categoria no encontrada')


@router.delete('/delete/{categoria_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(session: SessionDep, categoria_id: int = Path(gt=0)):
    categoria = session.get(Categoria, categoria_id)
    if categoria is not None:
        categoria.deleted_at = datetime.now()
        session.add(categoria)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Categoria no encontrada')
