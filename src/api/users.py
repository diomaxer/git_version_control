import datetime
from typing import List, Optional

from fastapi import APIRouter, status, Depends, Path

from src.api.protocols import UserServiceProtocol
from src.user.models import UserResponseV1, UserAddRequestV1, UserRepos

router = APIRouter(
    tags=['Users']
)


@router.get(
    path='/v1/users',
    response_model=List[UserResponseV1],
    summary='Список пользователей',
    description='Возвращает список всех пользователей.'
)
def get_all_users(
        user_service: UserServiceProtocol = Depends()
):
    return user_service.get_all_users()


@router.get(
    path='/v1/users/{id}',
    response_model=Optional[UserResponseV1],
    summary='Информация о пользователе',
    description='Возвращает информацию о пользователе.',
    responses={
            404: {
                "content": {"application/json": {"example": {"detail": "Пользователь не найден"}}},
            }}
)
def get_user(
        id: int = Path(..., ge=1),
        user_service: UserServiceProtocol = Depends()
):
    return user_service.get_user_by_id(id)


@router.post(
    path='/v1/users',
    status_code=status.HTTP_201_CREATED,
    summary='Добавить пользователя',
    description='Добавляет пользователя для отслеживания популярности репозиториев.',
)
def add_user(
        user_data: UserAddRequestV1,
        user_service: UserServiceProtocol = Depends()
):
    user_service.add_user(user_data)


@router.delete(
    path='/v1/users/{id}',
    summary='Удалить пользователя',
    description='Удаляет пользователя.',
)
def delete_user(
        id: int = Path(..., ge=1),
        user_service: UserServiceProtocol = Depends()
):
    user_service.delete_user_by_id(id)


@router.get(
    path='/v1/users/{id}/stat',
    response_model=Optional[UserRepos],
    summary='Информация о репозиториях пользователя',
    description='Возвращает информацию о репозиториях пользователе за определенный период.',
    responses={
            404: {
                "content": {"application/json": {"example": {"detail": "Пользователь не найден"}}},
            }}
)
def get_user_stats(
        id: int = Path(..., ge=1),
        date_from: Optional[datetime.date] = None,
        date_to: Optional[datetime.date] = None,
        user_service: UserServiceProtocol = Depends()
):
    return user_service.get_user_stat_by_id(id, date_from, date_to)
