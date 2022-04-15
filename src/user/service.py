from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.future import Engine
from starlette import status

from src.database import tables
from src.user.models import UserResponseV1, UserAddRequestV1


class UserService:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def get_all_users(self) -> List[UserResponseV1]:
        query = select(tables.users)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        users = []
        for user_data in users_data:
            user = UserResponseV1(
                id=user_data['id'],
                login=user_data['login'],
                name=user_data['name']
            )
            users.append(user)
        return users

    def get_user_by_id(self, id: int) -> Optional[UserResponseV1]:
        query = select(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            user_data = connection.execute(query)
            user_data = user_data.fetchone()
        if not user_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
        user = UserResponseV1(
            id=user_data['id'],
            login=user_data['login'],
            name=user_data['name']
        )
        return user

    def add_user(self, user: UserAddRequestV1) -> None:
        query = insert(tables.users).values(
            id=user.id,
            login=user.login,
            name=user.name
        )
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def delete_user_by_id(self, id: int) -> None:
        query = delete(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()
