from abc import ABC
from collections.abc import Mapping
from datetime import datetime
from typing import Final

import jwt

from memealerts.types.exceptions import MATokenExpired
from memealerts.types.user_id import UserID


class BaseMAClient(ABC):
    _BASE_URL: Final[str] = "https://memealerts.com/api"

    def __init__(self, token: str) -> None:
        token_parsed = jwt.decode(token, algorithms=["HS256"], options={"verify_signature": False})
        self.__streamer_user_id = token_parsed["id"]
        self.__token_expires_in = datetime.fromtimestamp(token_parsed['exp'])
        self.__token = token
        if self.__token_expires_in < datetime.now():
            raise MATokenExpired

    @property
    def streamer_user_id(self) -> UserID:
        return self.__streamer_user_id

    @property
    def _headers(self) -> Mapping[str, str]:
        return {"Authorization": f"Bearer {self.__token}"}