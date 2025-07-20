from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import httpx

from memealerts.base_client import BaseMAClient
from memealerts.types.encoder import replace_rootmodel_with_str
from memealerts.types.exceptions import MAError
from memealerts.types.models import Balance, SupportersList, User

if TYPE_CHECKING:
    from memealerts.types.user_id import UserID


class MemealertsAsyncClient(BaseMAClient):
    """
    Async клиент для Memealerts API.

    Особенности:
    - Persistent httpx.AsyncClient: создаётся в __init__, не закрывается после каждого запроса.
    - Можно использовать двумя способами:
        1. Контекстный менеджер:

            async with MemealertsAsyncClient(token) as cli:
                supporters = await cli.get_supporters()

        2. Долгоживущий объект:

            cli = MemealertsAsyncClient(token)
            supporters = await cli.get_supporters()
            ...
            await cli.aclose()

    - Если передан внешний AsyncClient (client=...), ответственность за закрытие на вызывающем коде.
    """

    def __init__(
        self,
        token: str,
        *,
        base_url: str | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> None:
        super().__init__(token)

        self._base_url = base_url or self._BASE_URL  # _BASE_URL в BaseMAClient
        self._client_provided = client is not None

        # Если клиент не передан, создаём свой. Хедеры добавляем сразу.
        self._client = client or httpx.AsyncClient(
            base_url=self._base_url,
            headers=self._headers,  # в BaseMAClient формируется Authorization и т.п.
            timeout=timeout,
        )

        self._closed = False  # сами закрыли или через __aexit__
        self._entered = False  # чтобы не закрывать дважды в __aexit__

    # ------------------------------------------------------------------ #
    #   Контекстный менеджер
    # ------------------------------------------------------------------ #
    async def __aenter__(self) -> MemealertsAsyncClient:
        self._entered = True
        self._ensure_open()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        # Закрываем только если клиент наш (не внешний)
        if not self._client_provided:
            await self.aclose()

    # ------------------------------------------------------------------ #
    #   Публичный метод закрытия
    # ------------------------------------------------------------------ #
    async def aclose(self) -> None:
        """Закрыть underlying httpx.AsyncClient (если он наш)."""
        if self._closed:
            return
        if not self._client_provided:
            await self._client.aclose()
        self._closed = True

    # ------------------------------------------------------------------ #
    #   Служебные
    # ------------------------------------------------------------------ #
    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("MemealertsAsyncClient is closed.")

    async def _post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        expected_status: int | None = None,
    ) -> httpx.Response:
        """
        Вспомогательный POST.

        expected_status=None  -> допускаем любой 2xx (через raise_for_status()).
        expected_status=HTTPStatus.CREATED -> проверяем вручную и бросаем MAError иначе.
        """
        self._ensure_open()
        json = replace_rootmodel_with_str(json)
        resp = await self._client.post(path, json=json)
        if expected_status is None:
            resp.raise_for_status()
        elif resp.status_code != expected_status:
            raise MAError(f"Unexpected status {resp.status_code} for {path}")
        return resp

    # ------------------------------------------------------------------ #
    #   API методы
    # ------------------------------------------------------------------ #
    async def get_supporters(
        self,
        limit: int | None = None,
        query: str | None = None,
        skip: int | None = None,
    ) -> SupportersList:
        params = {"limit": limit, "query": query, "skip": skip}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._post("/supporters", json=params, expected_status=None)
        return SupportersList.model_validate(resp.json())

    async def give_bonus(self, user: UserID, value: int) -> None:
        if value < 1:
            raise ValueError("Value must be more than 0")
        payload = {"userId": user, "streamerId": self.streamer_user_id, "value": value}
        payload = {k: v for k, v in payload.items() if v is not None}

        await self._post(
            self._BASE_URL + "/user/give-bonus",
            json=payload,
            expected_status=HTTPStatus.CREATED,
        )

    async def find_user(self, username: str) -> User:
        """
        Search for a user by username (which is user link actually, but not a name).
        """
        resp = await self._post("/user/find", json={"username": username}, expected_status=HTTPStatus.CREATED)
        return User.model_validate(resp.json())

    async def get_balance(self, username: str) -> Balance:
        """
        Shows you balance for your account at streamer `username` channel
        """
        resp = await self._post("/user/balance", json={"username": username}, expected_status=HTTPStatus.CREATED)
        return Balance.model_validate(resp.json())
