from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from starlette import status
from sqlmodel import select

from ..models import Resultado, ResultadoBase, ResultadoPublic
from ..database import SessionDep

router = APIRouter(
    prefix='/resultados',
    tags=['resultados']
)


@router.get('/', response_model=list[ResultadoPublic], status_code=status.HTTP_200_OK)
async def read_resultados(session: SessionDep):
    statement = select(Resultado).where(Resultado.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{resultado_id}')
async def busqueda(session: SessionDep, resultado_id: int):
    resultado_id = session.query(Resultado).where(Resultado.deleted_at == None).filter(Resultado.id == resultado_id).first()
    if resultado_id is not None:
        return resultado_id
    raise HTTPException(status_code=404, detail='Resultado no encontrado')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_resultado(session: SessionDep, resultado_request: ResultadoBase):
    resultado = Resultado.model_validate(resultado_request)
    session.add(resultado)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_resultado(session: SessionDep, resultado_request: ResultadoBase, id: int = Path(gt=0)):
    resultado = session.get(Resultado, id)
    if resultado is not None:
        resultado_data = resultado_request.model_dump(exclude_unset=True)
        resultado.updated_at = datetime.now()
        resultado.sqlmodel_update(resultado_data)
        session.add(resultado)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se encontro el resultado')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_resultado(session: SessionDep, id: int = Path(gt=0)):
    resultado = session.get(Resultado, id)
    if resultado is not None:
        resultado.deleted_at = None
        session.add(resultado)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Resultado no encontrado')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_resultado(session: SessionDep, id: int = Path(gt=0)):
    resultado = session.get(Resultado, id)
    if resultado is not None:
        resultado.deleted_at = datetime.now()
        session.add(resultado)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Resultado no encontrado')
