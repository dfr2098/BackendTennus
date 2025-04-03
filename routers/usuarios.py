from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from starlette import status
from sqlmodel import select

from ..models import Usuario, UsuarioBase, UsuarioPublic, UsuarioCreate
from ..database import SessionDep
from .auth import get_password_hash

router = APIRouter(
    prefix='/usuarios',
    tags=['usuarios']
)


@router.get('/', response_model=list[UsuarioPublic], status_code=status.HTTP_200_OK)
async def read_usuarios(session: SessionDep):
    statement = select(Usuario).where(Usuario.deleted_at == None)
    results = session.exec(statement).all()
    return results

@router.get('/{usuario_id}')
async def busqueda(session: SessionDep, usuario_id: int):
    usuario_id = session.query(Usuario).where(Usuario.deleted_at == None).filter(Usuario.id == usuario_id).first()
    if usuario_id is not None:
        return usuario_id
    raise HTTPException(status_code=404, detail='Usuario no encontrado')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_usuario(session: SessionDep, usuario_request: UsuarioCreate):
    usuario = Usuario.model_validate(usuario_request)
    usuario.hashed_password = get_password_hash(usuario_request.password)
    session.add(usuario)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_usuario(session: SessionDep, usuario_request: UsuarioBase, id: int = Path(gt=0)):
    usuario = session.get(Usuario, id)
    if usuario is not None:
        usuario_data = usuario_request.model_dump(exclude_unset=True)
        usuario.updated_at = datetime.now()
        usuario.sqlmodel_update(usuario_data)
        session.add(usuario)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se encontro el usuario')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_usuario(session: SessionDep, id: int = Path(gt=0)):
    usuario = session.get(Usuario, id)
    if usuario is not None:
        usuario.deleted_at = None
        session.add(usuario)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(session: SessionDep, id: int = Path(gt=0)):
    usuario = session.get(Usuario, id)
    if usuario is not None:
        usuario.deleted_at = datetime.now()
        session.add(usuario)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
