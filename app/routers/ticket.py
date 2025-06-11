from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.dependency import Dependency
from app.enums.status import StatusEnum
from app.models.ticket import Ticket
from app.schemas import ticket as schema_ticket

router = APIRouter(prefix=f"/tickets", tags=["ticket"])


def get_ticket(db: Session, ticket_id: UUID):
    db_ticket = Ticket.find(db=db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
        )
    return db_ticket


@router.post(
    "/",
    response_model=schema_ticket.Ticket,
    description="The endpoint to create a ticket with a title and a description. The status of the created ticket is 'open'.",
    response_description="The created ticket.",
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    ticket: schema_ticket.TicketBase, db: Session = Depends(Dependency.get_db)
):
    db_ticket = Ticket(**ticket.model_dump())
    db_ticket.save(db=db)
    return db_ticket


@router.get(
    "/",
    response_model=list[schema_ticket.Ticket],
    description="The endpoint to list all the tickets.",
    response_description="The list of the tickets.",
)
def list_ticket(db: Session = Depends(Dependency.get_db)):
    return db.query(Ticket)


@router.get(
    "/{ticket_id}",
    response_model=schema_ticket.Ticket,
    description="The endpoint to get the information of the ticket with the requested id.",
    response_description="The ticket.",
)
def read_ticket(ticket_id: UUID, db: Session = Depends(Dependency.get_db)):
    return get_ticket(db=db, ticket_id=ticket_id)


@router.put(
    "/{ticket_id}",
    response_model=schema_ticket.Ticket,
    description="The endpoint to update informations about the ticket with the requested id.",
    response_description="The updated ticket.",
)
def update_ticket(
    ticket_id: UUID,
    new_ticket: schema_ticket.TicketUpdate,
    db: Session = Depends(Dependency.get_db),
):
    db_ticket = get_ticket(db=db, ticket_id=ticket_id)
    if new_ticket.title:
        db_ticket.title = new_ticket.title
    if new_ticket.description:
        db_ticket.description = new_ticket.description
    if new_ticket.status:
        db_ticket.status = StatusEnum[new_ticket.status]
    db_ticket.save(db=db)
    return db_ticket


@router.patch(
    "/{ticket_id}/close",
    response_model=schema_ticket.Ticket,
    description="The endpoint to close the ticket with the requested id.",
    response_description="The closed ticket.",
)
def close_ticket(ticket_id: UUID, db: Session = Depends(Dependency.get_db)):
    db_ticket = get_ticket(db=db, ticket_id=ticket_id)
    db_ticket.status = StatusEnum.closed
    db_ticket.save(db=db)
    return db_ticket
