from fastapi import APIRouter
from starlette import status
from sqlmodel import select

from ..models import EstadoBase, Estado, EstadoPublic
from ..database import SessionDep

router = APIRouter(
    prefix='/estados',
    tags=['estados']
)


@router.get('/', response_model=list[EstadoPublic], status_code=status.HTTP_200_OK)
async def read_estados(session: SessionDep):
    statement = select(Estado)
    results = session.exec(statement).all()
    return results