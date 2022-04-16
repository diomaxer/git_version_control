import sqlalchemy as sa
from fastapi import FastAPI

import src.api.protocols
from src.api import users, protocols
from src.database import create_database_url
from src.database.settings import MyDataBase
from src.user.service import UserService


def get_application() -> FastAPI:
    application = FastAPI(
        title='GitHub Repo Stats',
        description='Сервис сбора статистических данных о популярности репозиториев на GitHub.',
        version='1.0.0'
    )

    application.include_router(users.router)

    db_settings = MyDataBase
    engine = sa.create_engine(
        create_database_url(db_settings),
        future=True
    )
    user_service = UserService(engine)
    application.dependency_overrides[protocols.UserServiceProtocol] = lambda: user_service
    return application


app = get_application()
