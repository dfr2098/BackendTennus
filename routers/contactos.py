from fastapi import APIRouter, Path
from fastapi_mail import MessageSchema, MessageType
from starlette import status

from sqlmodel import select
from ..database import SessionDep
from ..models import ContactoPublic, Contacto, ContactoBase
from ..config import MailConfigDep, ConfigDep

router = APIRouter(
    prefix='/contactos',
    tags=['contactos']
)


@router.get('/', response_model=list[ContactoPublic], status_code=status.HTTP_200_OK)
async def read_contacto(session: SessionDep):
    statement = select(Contacto).where(Contacto.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_contacto(session: SessionDep, fm: MailConfigDep, config: ConfigDep, contacto_request: ContactoBase):
    contacto = Contacto.model_validate(contacto_request)
    session.add(contacto)
    session.commit()

    html = "".format(
        nombre=contacto.nombre, apellidos=contacto.apellidos, telefono=contacto.telefono, correo=contacto.correo,
        comentario=contacto.comentario)

    message = MessageSchema(
        subject="Buzón de contacto TENNUS",
        recipients=[config.contacto_email],
        template_body=contacto.model_dump(),
        subtype=MessageType.html)

    await fm.send_message(message, template_name='contacto.html')
