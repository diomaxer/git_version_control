from typing import List, Optional
import datetime
from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.future import Engine
from starlette import status

from src.database import tables
from src.user.models import UserResponseV1, UserAddRequestV1, UserRepos, UserStatMin


class UserService:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def get_all_users(self) -> List[UserResponseV1]:
        query = select(tables.users)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        users = []
        for user_data in users_data:
            print(type(user_data))
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

    def get_user_stat_by_id(self, id: int, date_from: Optional[datetime.date], date_to: Optional[datetime.date]) -> Optional[UserRepos]:
        user = self.get_user_by_id(id)
        query = select(tables.stats).where(tables.stats.c.user_id == id)
        if date_from:
            query = query.where(tables.stats.c.date >= date_from)
        if date_to:
            query = query.where(tables.stats.c.date <= date_to)
        with self._engine.connect() as connection:
            user_data = connection.execute(query)
        if not user_data:
            stats = None
        else:
            stats = []
            for row in user_data:
                stat = UserStatMin(
                    repo_id=row['repo_id'],
                    date=row['date'],
                    stargazers=row['stargazers'],
                    forks=row['forks'],
                    watchers=row['watchers'],
                )
                stats.append(stat)
        return UserRepos(user=user, stats=stats)
