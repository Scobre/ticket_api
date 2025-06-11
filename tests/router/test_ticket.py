import pytest
import pytest_check as check
from fastapi import status

from app.enums.status import StatusEnum
from app.models.ticket import Ticket
from tests.test_main import TestClient, TestingSessionLocal, client, session


@pytest.fixture(params=["created", "miss_title", "miss_description"])
def _fake_create_ticket(request, session: TestingSessionLocal):
    return_json = {}
    ticket = {}
    title = "The title of the ticket"
    description = "The description of the ticket"
    if request.param == "created":
        return_json["status_code"] = status.HTTP_201_CREATED
        ticket["title"] = title
        ticket["description"] = description
    elif request.param == "miss_title":
        return_json["status_code"] = status.HTTP_422_UNPROCESSABLE_ENTITY
        ticket["description"] = description
    elif request.param == "miss_description":
        return_json["status_code"] = status.HTTP_422_UNPROCESSABLE_ENTITY
        ticket["title"] = title
    return_json["ticket"] = ticket
    return return_json


@pytest.fixture(params=["empty_list", "with_tickets"])
def _fake_list_ticket(request, session: TestingSessionLocal):
    return_json = {}
    return_json["status_code"] = status.HTTP_200_OK
    if request.param == "empty_list":
        return_json["tickets"] = []
    else:
        ticket1 = Ticket(
            title="First ticket", description="Description of the first ticket"
        )
        ticket2 = Ticket(
            title="Second ticket",
            description="Description of the second ticket",
            status=StatusEnum.stalled,
        )
        ticket3 = Ticket(
            title="Last ticket",
            description="Description of the second ticket",
            status=StatusEnum.closed,
        )
        ticket1.save(session)
        ticket2.save(session)
        ticket3.save(session)
        return_json["tickets"] = [ticket1, ticket2, ticket3]
    return return_json


@pytest.fixture(params=["wrong_uuid", "not_uuid", "find_ticket"])
def _fake_read_ticket(request, session: TestingSessionLocal):
    return_json = {}
    if request.param == "wrong_uuid":
        return_json["status_code"] = status.HTTP_404_NOT_FOUND
        return_json["ticket"] = {"detail": "Ticket not found"}
        return_json["ticket_id"] = "7490e4ab-564e-4182-ba83-92dc72e042a5"
    elif request.param == "not_uuid":
        return_json["status_code"] = status.HTTP_422_UNPROCESSABLE_ENTITY
        return_json["ticket_id"] = "7490e4ab-564e-4182-ba83-"
    else:
        ticket = Ticket(
            id="7490e4ab-564e-4182-ba83-92dc72e042a5",
            title="My ticket",
            description="Description of my ticket",
        )
        ticket.save(session)
        return_json["status_code"] = status.HTTP_200_OK
        return_json["ticket_id"] = "7490e4ab-564e-4182-ba83-92dc72e042a5"
        return_json["ticket"] = {
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "status": ticket.status.value,
            "created_at": ticket.created_at.isoformat(),
        }
    return return_json


@pytest.fixture(params=["wrong_uuid", "not_uuid", "change"])
def _fake_update_ticket(request, session: TestingSessionLocal):
    new_title = "New title"
    new_description = "The new description of the ticket"
    new_status = StatusEnum.stalled.value
    return_json = {
        "params": {
            "title": new_title,
            "description": new_description,
            "status": new_status,
        }
    }
    if request.param == "wrong_uuid":
        return_json["status_code"] = status.HTTP_404_NOT_FOUND
        return_json["ticket"] = {"detail": "Ticket not found"}
        return_json["ticket_id"] = "7490e4ab-564e-4182-ba83-92dc72e042a5"
    elif request.param == "not_uuid":
        return_json["status_code"] = status.HTTP_422_UNPROCESSABLE_ENTITY
        return_json["ticket_id"] = "7490e4ab-564e-4182-ba83-"
    else:
        ticket = Ticket(
            id="7490e4ab-564e-4182-ba83-92dc72e042a5",
            title="My ticket",
            description="Description of my ticket",
        )
        ticket.save(session)
        return_json["status_code"] = status.HTTP_200_OK
        return_json["ticket_id"] = "7490e4ab-564e-4182-ba83-92dc72e042a5"
        return_json["ticket"] = {
            "id": ticket.id,
            "title": new_title,
            "description": new_description,
            "status": new_status,
            "created_at": ticket.created_at.isoformat(),
        }
    return return_json


@pytest.fixture(params=["wrong_uuid", "not_uuid", "close"])
def _fake_close_ticket(request, session: TestingSessionLocal):
    return_json = {}
    if request.param == "wrong_uuid":
        return_json["status_code"] = status.HTTP_404_NOT_FOUND
        return_json["ticket"] = {"detail": "Ticket not found"}
        return_json["ticket_id"] = "7490e4ab-564e-4182-ba83-92dc72e042a5"
    elif request.param == "not_uuid":
        return_json["status_code"] = status.HTTP_422_UNPROCESSABLE_ENTITY
        return_json["ticket_id"] = "7490e4ab-564e-4182-ba83-"
    else:
        ticket = Ticket(
            id="7490e4ab-564e-4182-ba83-92dc72e042a5",
            title="My ticket",
            description="Description of my ticket",
        )
        ticket.save(session)
        return_json["status_code"] = status.HTTP_200_OK
        return_json["ticket_id"] = "7490e4ab-564e-4182-ba83-92dc72e042a5"
        return_json["ticket"] = {
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "status": StatusEnum.closed.value,
            "created_at": ticket.created_at.isoformat(),
        }
    return return_json


def test_create_ticket(
    client: TestClient, session: TestingSessionLocal, _fake_create_ticket: dict
):
    response = client.post("/tickets/", json=_fake_create_ticket["ticket"])
    check.equal(response.status_code, _fake_create_ticket["status_code"])
    if response.status_code == status.HTTP_201_CREATED:
        check.equal(response.json()["title"], _fake_create_ticket["ticket"]["title"])
        check.equal(
            response.json()["description"], _fake_create_ticket["ticket"]["description"]
        )
        check.equal(response.json()["status"], "open")
        check.is_in("id", response.json())
        check.is_in("created_at", response.json())


def test_list_ticket(
    client: TestClient, session: TestingSessionLocal, _fake_list_ticket: dict
):
    response = client.get("/tickets/")
    check.equal(response.status_code, _fake_list_ticket["status_code"])
    check.equal(len(response.json()), len(_fake_list_ticket["tickets"]))


def test_read_ticket(
    client: TestClient, session: TestingSessionLocal, _fake_read_ticket: dict
):
    response = client.get(f"/tickets/{_fake_read_ticket['ticket_id']}")
    check.equal(response.status_code, _fake_read_ticket["status_code"])
    if "ticket" in _fake_read_ticket:
        check.equal(response.json(), _fake_read_ticket["ticket"])


def test_update_ticket(
    client: TestClient, session: TestingSessionLocal, _fake_update_ticket: dict
):
    response = client.put(
        f"/tickets/{_fake_update_ticket['ticket_id']}",
        json=_fake_update_ticket["params"],
    )
    check.equal(response.status_code, _fake_update_ticket["status_code"])
    if "ticket" in _fake_update_ticket:
        check.equal(response.json(), _fake_update_ticket["ticket"])


def test_close_ticket(
    client: TestClient, session: TestingSessionLocal, _fake_close_ticket: dict
):
    response = client.patch(f"/tickets/{_fake_close_ticket['ticket_id']}/close")
    check.equal(response.status_code, _fake_close_ticket["status_code"])
    if "ticket" in _fake_close_ticket:
        check.equal(response.json(), _fake_close_ticket["ticket"])
