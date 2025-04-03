from datetime import datetime

from fastapi import APIRouter, HTTPException, Path
from starlette import status
from sqlmodel import select

from ..models import FormaPagoBase, FormaPago, FormaPagoPublic
from ..database import SessionDep

router = APIRouter(
    prefix='/forma_pago',
    tags=['forma de pago']
)


@router.get('/', response_model=list[FormaPagoPublic], status_code=status.HTTP_200_OK)
async def read_forma_pago(session: SessionDep):
    statement = select(FormaPago).where(FormaPago.deleted_at == None)
    results = session.exec(statement).all()
    return results


@router.get('/{forma_pago_id}')
async def busqueda(session: SessionDep, forma_pago_id: int):
    forma_pago_id = session.query(FormaPago).where(FormaPago.deleted_at == None).filter(FormaPago.id == forma_pago_id).first()
    if forma_pago_id is not None:
        return forma_pago_id
    raise HTTPException(status_code=404, detail='Forma de pago no encontrada')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_forma_pago(session: SessionDep, forma_request: FormaPagoBase):
    print(forma_request)
    forma = FormaPago.model_validate(forma_request)

    session.add(forma)
    session.commit()


@router.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_forma(session: SessionDep, forma_request: FormaPagoBase, id: int = Path(gt=0)):
    forma = session.get(FormaPago, id)
    if forma is not None:
        forma_data = forma_request.model_dump(exclude_unset=True)
        forma.updated_at = datetime.now()
        forma.sqlmodel_update(forma_data)
        session.add(forma)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='No se encontro la forma de pago')


@router.put('/restore/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def restore_forma(session: SessionDep, id: int = Path(gt=0)):
    forma = session.get(FormaPago, id)
    if forma is not None:
        forma.deleted_at = None
        session.add(forma)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Forma de pago no encontrada')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_forma(session: SessionDep, id: int = Path(gt=0)):
    forma = session.get(FormaPago, id)
    print(forma)
    if forma is not None:
        forma.deleted_at = datetime.now()
        session.add(forma)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Forma de pago no encontrada')
