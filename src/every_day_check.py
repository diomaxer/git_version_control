import sys
import datetime
import time

import schedule

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from user.models import UserResponseV1, UserStat
import httpx

sys.path = ['', '..'] + sys.path[1:]

from src.database.db import engine
from src.database import tables

conn = engine.connect()


def get_users():
    """
    Получение всех зарегистрированных пользователей
    """
    query = select(tables.users)
    result = conn.execute(query)
    users = []
    for user_data in result:
        user = UserResponseV1(
            id=user_data['id'],
            login=user_data['login'],
            name=user_data['name']
        )
        users.append(user)
    return users


def get_users_data_from_api(users):
    """
    Получение данных репозиториев пользователей
    """
    all_user_data = []
    for user in users:
        repos = httpx.get(f'https://api.github.com/users/{user.login}/repos')
        print(repos.status_code)
        if repos.status_code != 200:
            print('API rate limit exceeded')
            raise ConnectionError
        for r in repos.json():
            user_stat = UserStat(
                user_id=user.id,
                repo_id=r['id'],
                date=datetime.datetime.fromisoformat(r['created_at'][:-1]).astimezone(datetime.timezone.utc).strftime('%Y-%m-%d'),
                stargazers=r['stargazers_count'],
                forks=r['forks_count'],
                watchers=r['watchers_count']
            )
            all_user_data.append(user_stat)
    return all_user_data


def insert_data(all_users_data):
    """
    Запись бд новых репозиториев
    """
    val = [item.__dict__ for item in all_users_data]
    insert_stmt = insert(tables.stats).values(val)
    on_duplicate_key_stmt = insert_stmt.on_conflict_do_update(
        index_elements=['repo_id'],
        set_={
            'repo_id': insert_stmt.excluded.repo_id,
            'date': insert_stmt.excluded.date,
            'stargazers': insert_stmt.excluded.stargazers,
            'forks': insert_stmt.excluded.forks,
            'watchers': insert_stmt.excluded.watchers,
        }
    )
    conn.execute(on_duplicate_key_stmt)


def do_the_job():
    """
    Функция для записи в cron
    """
    users = get_users()
    all_users_data = get_users_data_from_api(users)
    if all_users_data:
        insert_data(all_users_data)


if __name__ == '__main__':
    schedule.every().day.at("00:00").do(do_the_job)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except ConnectionError:
            print('Wait 30 minutes')
            while True:
                try:
                    print('30 min sleep')
                    time.sleep(60*30)
                    do_the_job()
                    break
                except ConnectionError:
                    continue


