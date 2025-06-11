from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.enums.status import StatusEnum


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Literal[StatusEnum.stalled.value] | None = None


class TicketBase(BaseModel):
    title: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ] = Field()
    description: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ] = Field()


class Ticket(TicketBase):
    id: UUID
    created_at: datetime
    status: StatusEnum
    model_config = ConfigDict(from_attributes=True)
