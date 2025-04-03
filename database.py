from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session, Field, Relationship, SQLModel

from .config import ConfigDep, get_config
from . import models

db_config: ConfigDep = get_config()



mysql_url = 'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'.format(
    db_user=db_config.db_user,
    db_password=db_config.db_password,
    db_host=db_config.db_host,
    db_name=db_config.db_name,
    db_port=db_config.db_port
)
engine = create_engine(mysql_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
