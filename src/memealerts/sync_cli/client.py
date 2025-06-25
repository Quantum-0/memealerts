import requests

from memealerts.base_client import BaseMAClient
from memealerts.types.exceptions import MAError
from memealerts.types.models import SupportersList
from memealerts.types.user_id import UserID


class MemealertsClient(BaseMAClient):
    def __init__(self, token: str):
        super().__init__(token)

    def get_supporters(
        self,
        limit: int | None = None,
        query: str | None = None,
        skip: int | None = None
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
        if response.status_code != 201:
            raise MAError
