from typing import List, Optional

from src.user.models import UserResponseV1, UserAddRequestV1, UserRepos


class UserServiceProtocol:
    def get_all_users(self) -> List[UserResponseV1]:
        raise NotImplementedError

    def get_user_by_id(self, id: int) -> Optional[UserResponseV1]:
        raise NotImplementedError

    def get_user_stat_by_id(self, id: int) -> Optional[UserRepos]:
        raise NotImplementedError

    def add_user(self, user: UserAddRequestV1) -> None:
        raise NotImplementedError

    def delete_user_by_id(self, id: int) -> None:
        raise NotImplementedError
