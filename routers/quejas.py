from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from fastapi_mail import MessageType, MessageSchema
from sqlmodel import select
from starlette import status

from ..config import MailConfigDep, ConfigDep
from ..database import SessionDep
from ..models import Queja, QuejaPublic, QuejaBase

router = APIRouter(
    prefix='/quejas',
    tags=['quejas']
)


@router.get('/', response_model=list[QuejaPublic], status_code=status.HTTP_200_OK)
async def read_quejas(session: SessionDep):
    statement = select(Queja).where(Queja.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_queja(session: SessionDep, fm: MailConfigDep, config: ConfigDep, queja_request: QuejaBase):
    queja = Queja.model_validate(queja_request)
    session.add(queja)
    session.commit()

    html = "".format(
        nombre=queja.nombre, correo=queja.correo, observacion=queja.observacion)

    message = MessageSchema(
        subject="Buzón de quejas TENNUS",
        recipients=[config.quejas_email],
        template_body=queja.model_dump(),
        subtype=MessageType.html)

    await fm.send_message(message, template_name='queja.html')


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_queja(session: SessionDep, queja_request: QuejaBase, id: int = Path(gt=0)):
    queja = session.get(Queja, id)
    if queja is not None:
        queja_data = queja_request.model_dump(exclude_unset=True)
        queja.updated_at = datetime.now()
        queja.sqlmodel_update(queja_data)
        session.add(queja)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se encontro la queja')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_queja(session: SessionDep, id: int = Path(gt=0)):
    queja = session.get(Queja, id)
    if queja is not None:
        queja.deleted_at = None
        session.add(queja)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Queja no encontrada')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_queja(session: SessionDep, id: int = Path(gt=0)):
    queja = session.get(Queja, id)
    if queja is not None:
        queja.deleted_at = datetime.now()
        session.add(queja)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Queja no encontrada')
