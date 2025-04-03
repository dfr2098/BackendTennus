from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from starlette import status
from sqlmodel import select

from ..models import RolBase, RolPublic, Rol
from ..database import SessionDep

router = APIRouter(
    prefix='/roles',
    tags=['roles']
)


@router.get('/', response_model=list[RolPublic], status_code=status.HTTP_200_OK)
async def read_roles(session: SessionDep):
    statement = select(Rol).where(Rol.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{rol_id}')
async def busqueda(session: SessionDep, rol_id: int):
    rol_id = session.query(Rol).where(Rol.deleted_at == None).filter(Rol.id == rol_id).first()
    if rol_id is not None:
        return rol_id
    raise HTTPException(status_code=404, detail='Rol no encontrado')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_rol(session: SessionDep, rol_request: RolBase):
    rol = Rol.model_validate(rol_request)
    session.add(rol)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_rol(session: SessionDep, rol_request: RolBase, id: int = Path(gt=0)):
    rol = session.get(Rol, id)
    if rol is not None:
        rol_data = rol_request.model_dump(exclude_unset=True)
        rol.updated_at = datetime.now()
        rol.sqlmodel_update(rol_data)
        session.add(rol)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se encontro el rol')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_rol(session: SessionDep, id: int = Path(gt=0)):
    rol = session.get(Rol, id)
    if rol is not None:
        rol.deleted_at = None
        session.add(rol)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Rol no encontrado')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_rol(session: SessionDep, id: int = Path(gt=0)):
    rol = session.get(Rol, id)
    print(rol)
    if rol is not None:
        rol.deleted_at = datetime.now()
        session.add(rol)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Rol no encontrado')
