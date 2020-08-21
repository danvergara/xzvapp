"""
This is the test suite of the app
I have no personal AWS account, so I'm
gonna mock the boto3 library with
pytest's monkeypatching.
"""

import boto3
import pytest

from app import app


@pytest.fixture(scope="module")
def test_app():
    """
    Flask provides a way to test your application by
    exposing the Werkzeug test client and handling
    the context locasl for you
    """
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


class MockClient():
    """custom class to be the mock return value of client"""
    def get_item(self, *args, **kwargs):
        """mocks the get_item method"""
        return {
            "Item": {
                "userId": {
                    "S": "user1",
                },
                "name": {
                    "S": "Dan Vergara",
                },
            },
        }

    def put_item(self, *args, **kwargs):
        """mocks the put_item method"""
        return {
            "Item": {
                "userId": {
                    "S": "user1",
                },
                "name": {
                    "S": "Dan Omar Vergara",
                },
            },
        }

    def update_item(self, *args, **kwargs):
        """mocks the update_item method"""
        return {
            "Attributes": {
                "userId": {
                    "S": "user1",
                },
                "name": {
                    "S": "Dan Perez",
                },
            },
        }

    def delete_item(self, *args, **kwargs):
        """mocks the update_item method"""
        return {
            "Attributes": {
                "userId": {
                    "S": "user1",
                },
                "name": {
                    "S": "Dan Vergara",
                },
            },
        }


@pytest.fixture
def mock_client(monkeypatch):
    """mock boto3 client"""
    def mock_client(*args, **kwargs):
        return MockClient()

    monkeypatch.setattr(
        boto3, "client", mock_client,
    )


def test_index(test_app):
    """test the index of the app"""
    response = test_app.get("/")
    assert response.status_code == 200


def test_get_user(test_app, mock_client):
    """test the get user endpoint"""
    response = test_app.get("/users/1")

    assert response.status_code == 200
    assert response.json.get("userId") == "user1"
    assert response.json.get("name") == "Dan Vergara"


def test_create_user(test_app, mock_client):
    """test the create user endpoint"""
    response = test_app.post(
        "/users", json={"userId": "user1", "name": "Dan Omar Vergara"},
    )

    assert response.status_code == 200
    assert response.json.get("userId") == "user1"
    assert response.json.get("name") == "Dan Omar Vergara"


def test_update_user(test_app, mock_client):
    """test the update user endpoint"""
    response = test_app.patch(
        "/users/1", json={"userId": "user1", "name": "Dan Perez"},
    )

    assert response.status_code == 200
    assert response.json.get("userId") == "user1"
    assert response.json.get("name") == "Dan Perez"


def test_delete_user(test_app, mock_client):
    """test the get user endpoint"""
    response = test_app.delete("/users/1")

    assert response.status_code == 200
    assert response.json.get("userId") == "user1"
    assert response.json.get("name") == "Dan Vergara"
