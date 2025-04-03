from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status
from sqlmodel import select

from ..models import ColoniaBase, Colonia, ColoniaPublic
from ..database import SessionDep

router = APIRouter(
    prefix='/colonias',
    tags=['colonias']
)


@router.get('/', response_model=list[ColoniaPublic], status_code=status.HTTP_200_OK)
async def read_colonias(session: SessionDep, codigo_postal: str = Query(min_length=3, max_length=5)):
    statement = select(Colonia).where(Colonia.codigo_postal.startswith(codigo_postal))
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No se encontro la colonia por el código postal')
    return results
