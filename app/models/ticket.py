from uuid import UUID, uuid4

from sqlalchemy import TIMESTAMP, Column, Enum, PrimaryKeyConstraint, String
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.config.database import Base
from app.enums.status import StatusEnum


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
        unique=True,
        nullable=False,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.open)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    PrimaryKeyConstraint("id")

    def save(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)
        return True

    @classmethod
    def find(cls, db: Session, ticket_id: UUID):
        return db.query(cls).where(cls.id.is_(str(ticket_id))).first()
