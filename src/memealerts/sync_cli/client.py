from http import HTTPStatus

import requests

from memealerts.base_client import BaseMAClient
from memealerts.types.exceptions import MAError
from memealerts.types.models import Balance, SupportersList, User
from memealerts.types.user_id import StickerID, UserID


class MemealertsClient(BaseMAClient):
    def __init__(self, token: str) -> None:
        super().__init__(token)

    def get_supporters(
        self, limit: int | None = None, query: str | None = None, skip: int | None = None
    ) -> SupportersList:
        query_params = {"limit": limit, "query": query, "skip": skip}
        query_params = {k: v for k, v in query_params.items() if v is not None}
        response = requests.post(
            self._BASE_URL + "/supporters",
            json=query_params,
            headers=self._headers,
        )
        return SupportersList.model_validate(response.json())

    def give_bonus(
        self,
        user: UserID,
        value: int,
    ) -> None:
        if value < 1:
            raise ValueError("Value must be more than 0")
        query_params = {"userId": user, "streamerId": self.streamer_user_id, "value": value}
        query_params = {k: v for k, v in query_params.items() if v is not None}
        response = requests.post(
            self._BASE_URL + "/user/give-bonus",
            json=query_params,
            headers=self._headers,
        )
        if response.status_code != HTTPStatus.CREATED:
            raise MAError

    def find_user(self, username: str) -> User:
        """
        Search for a user by username (which is user link actually, but not a name).
        """

        response = requests.post(
            self._BASE_URL + "/user/find",
            json={"username": username},
            headers=self._headers,
        )
        if response.status_code == HTTPStatus.CREATED:
            return User.model_validate(response.json())
        raise MAError

    def get_balance(self, username: str) -> Balance:
        """
        Shows you balance for your account at streamer `username` channel
        """
        response = requests.post(
            self._BASE_URL + "/user/balance",
            json={"username": username},
            headers=self._headers,
        )
        if response.status_code == HTTPStatus.CREATED:
            return Balance.model_validate(response.json())
        raise MAError

    def send_meme(
        self,
        to_channel: UserID,
        sticker_id: StickerID,
        *,
        is_sound_only: bool = False,
    ) -> None:
        raise NotImplementedError
        query_params = {
            "toChannel": to_channel,
            "stickerId": sticker_id,
            "isSoundOnly": is_sound_only,
            # "name": "quantum075",  # noqa: ERA001
            "deviceType": "desktop",
            "isMemePartyActive": False,
            "message": "",
            "topic": "Last",
            # TODO: not sure other fields are really needed o.o
            # FIXME: doesnt work
        }
        query_params = {k: v for k, v in query_params.items() if v is not None}
        response = requests.post(
            self._BASE_URL + "/sticker/send",
            json=query_params,
            headers=self._headers,
        )
        response.raise_for_status()
        if response.status_code != HTTPStatus.CREATED:
            raise MAError
