from datetime import datetime

from pydantic import BaseModel, AnyHttpUrl, field_validator
from pydantic import NonNegativeInt
from pydantic_core.core_schema import ValidationInfo

from memealerts.types.user_id import UserID


class Supporter(BaseModel):
    _id: UserID
    balance: NonNegativeInt
    welcomeBonusEarned: bool
    newbieActionUsed: bool
    spent: NonNegativeInt
    purchased: NonNegativeInt
    joined: datetime
    lastSupport: datetime
    supporterName: str
    supporterAvatar: AnyHttpUrl
    supporterLink: str
    supporterId: UserID
    mutes: list
    mutedByStreamer: bool

    @field_validator("supporterAvatar", mode="before")
    def put_full_avatar_link(cls, v: AnyHttpUrl | str, _: ValidationInfo) -> AnyHttpUrl:
        if v.startswith("media/"):
            return AnyHttpUrl("https://memealerts.com/" + v)
        return v

class SupportersList(BaseModel):
    data: list[Supporter]
    total: NonNegativeInt