from typing import Annotated

from pydantic import RootModel, StringConstraints


class UserID(RootModel[Annotated[str, StringConstraints(pattern='^[0-9a-f]{24}$')]]):
    def __init__(self, user_id: str) -> None:
        super().__init__(user_id)