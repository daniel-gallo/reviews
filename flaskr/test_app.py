import os
import re
import sqlite3
from contextlib import closing

import pytest

from app import app as app_, implementations
from emailsender import FakeEmailSender


def create_temporary_database(db_path):
    with open("../init.sql", "r") as f:
        init_script = f.read()

    with sqlite3.connect(str(db_path)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.executescript(init_script)


@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / "test.sqlite"
    create_temporary_database(db_path)

    os.environ["DATABASE_URL"] = str(db_path)
    app_.config.update({"TESTING": True})
    implementations.email_sender = FakeEmailSender()
    yield app_

    db_path.unlink()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get("/")
    data = response.data.decode()

    assert "Course name" in data
    assert "Rating" in data
    assert "Difficulty" in data

    assert "Computer Vision 1" in data


def test_existing_course(client):
    response = client.get("/CV1")
    data = response.data.decode()

    assert "Computer Vision 1" in data
    assert 'href="/CV1/add-review"' in data


def test_non_existing_course(client):
    response = client.get("/totally-made-up-code")

    print(response.data.decode())

    assert response.status_code == 404


def test_review(client):
    client.post(
        "/CV1/add-review",
        data={
            "email": "user@student.uva.nl",
            "nickname": "nickname",
            "year": "2022/2023",
            "rating": 9,
            "difficulty": 7,
            "workload": 15,
            "review": "Very good course",
        },
    )

    # The review has not been verified yet
    assert "Very good course" not in client.get("/CV1").data.decode()

    # Verify review
    sent_email = implementations.email_sender.sent_messages[-1]
    code = re.search(
        r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
        sent_email["body"],
    ).group(1)
    client.post("/verify-email", data=dict(code=code))

    # The review has been verified, so it should appear
    assert "Very good course" in client.get("/CV1").data.decode()
