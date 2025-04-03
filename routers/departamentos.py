from fastapi import APIRouter, Path, HTTPException
from starlette import status
from datetime import datetime
from sqlmodel import select

from ..models import DepartamentoPublic, Departamento, DepartamentoBase
from ..database import SessionDep

router = APIRouter(
    prefix='/departamentos',
    tags=['departamentos']
)


@router.get('/', response_model=list[DepartamentoPublic], status_code=status.HTTP_200_OK)
async def read_departamento(session: SessionDep):
    statement = select(Departamento).where(Departamento.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{departamento_id}')
async def busqueda(session: SessionDep, departamento_id: int):
    departamento_id = session.query(Departamento).where(Departamento.deleted_at == None).filter(Departamento.id == departamento_id).first()
    if departamento_id is not None:
        return departamento_id
    raise HTTPException(status_code=404, detail='Departamento no encontrado')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_departamento(session: SessionDep, departamento_request: DepartamentoBase):
    departamento = Departamento.model_validate(departamento_request)
    session.add(departamento)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_producto(session: SessionDep, departamento_request: DepartamentoBase, id: int = Path(gt=0)):
    departamento = session.get(Departamento, id)
    if departamento is not None:
        departamento_data = departamento_request.model_dump(exclude_unset=True)
        departamento.updated_at = datetime.now()
        departamento.sqlmodel_update(departamento_data)
        session.add(departamento)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Departamento no encontrado')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_departamento(session: SessionDep, id: int = Path(gt=0)):
    departamento = session.get(Departamento, id)
    if departamento is not None:
        departamento.deleted_at = None
        session.add(departamento)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Departamento no encontrado')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_departamento(session: SessionDep, id: int = Path(gt=0)):
    departamento = session.get(Departamento, id)
    if departamento is not None:
        departamento.deleted_at = datetime.now()
        session.add(departamento)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
