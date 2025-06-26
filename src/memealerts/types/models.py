from datetime import datetime

from memealerts.types.user_id import UserID
from pydantic import AnyHttpUrl, BaseModel, Field, NonNegativeInt, field_validator
from pydantic_core.core_schema import ValidationInfo


class Supporter(BaseModel):
    _id: UserID
    balance: NonNegativeInt
    welcome_bonus_earned: bool = Field(..., alias="welcomeBonusEarned")
    newbie_action_used: bool = Field(..., alias="newbieActionUsed")
    spent: NonNegativeInt
    purchased: NonNegativeInt
    joined: datetime
    last_support: datetime = Field(..., alias="lastSupport")
    supporter_name: str = Field(..., alias="supporterName")
    supporter_avatar: AnyHttpUrl = Field(..., alias="supporterAvatar")
    supporter_link: str = Field(..., alias="supporterLink")
    supporter_id: UserID = Field(..., alias="supporterId")
    mutes: list
    muted_by_streamer: bool = Field(..., alias="mutedByStreamer")

    @field_validator("supporter_avatar", mode="before")
    def put_full_avatar_link(cls, v: AnyHttpUrl | str, _: ValidationInfo) -> AnyHttpUrl | str:  # noqa: N805
        if isinstance(v, str) and v.startswith("media/"):
            return AnyHttpUrl("https://memealerts.com/" + v)
        return v


class SupportersList(BaseModel):
    data: list[Supporter]
    total: NonNegativeInt
