from passlib.context import CryptContext
import jwt
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException, status
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from sqlmodel import select

from ..models import Usuario, TokenData, Token
from ..config import ConfigDep
from ..database import SessionDep

router = APIRouter(
    prefix='/auth',
    tags=['autorizacion']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: SessionDep, correo: str, password: str):
    statement = select(Usuario).where(Usuario.deleted_at == None).where(Usuario.correo == correo)
    results = db.exec(statement)
    user = results.first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(config: ConfigDep, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_token, algorithm=config.algorithm)
    return encoded_jwt


async def get_current_user(db: SessionDep, config: ConfigDep, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.secret_token, algorithms=[config.algorithm])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
        token_data = TokenData(username=correo)
    except InvalidTokenError:
        raise credentials_exception
    statement = select(Usuario).where(Usuario.deleted_at == None).where(Usuario.correo == token_data.username)
    results = db.exec(statement)
    user = results.first()
    if user is None:
        raise credentials_exception
    return user

AuthDependency = Annotated[Usuario, Depends(get_current_user)]

@router.post("/token")
async def login_for_access_token(db: SessionDep, config: ConfigDep,
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 ) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.access_token_expire)
    access_token = create_access_token(
        config,
        data={"sub": user.correo}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=Usuario)
async def read_users_me(
    current_user: AuthDependency,
):
    return current_user

