from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from fastapi.openapi.models import PathItem
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi_mail import FastMail, MessageType, MessageSchema, ConnectionConfig


class Config(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    db_port: int

    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str
    mail_starttls: bool
    mail_ssl_tls: bool
    use_credentials: bool
    validate_certs: bool

    quejas_email: str
    contacto_email: str

    secret_token: str
    algorithm: str
    access_token_expire: int

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_config():
    return Config()


ConfigDep = Annotated[Config, Depends(get_config)]


def get_mail_config(config: ConfigDep):
    return FastMail(ConnectionConfig(
        MAIL_USERNAME=config.mail_username,
        MAIL_PASSWORD=config.mail_password,
        MAIL_FROM=config.mail_from,
        MAIL_PORT=config.mail_port,
        MAIL_SERVER=config.mail_server,
        MAIL_FROM_NAME=config.mail_from_name,
        MAIL_STARTTLS=config.mail_starttls,
        MAIL_SSL_TLS=config.mail_ssl_tls,
        USE_CREDENTIALS=config.use_credentials,
        VALIDATE_CERTS=config.validate_certs,
        TEMPLATE_FOLDER=Path(__file__).parent / 'emails',
    ))


MailConfigDep = Annotated[FastMail, Depends(get_mail_config)]
