"""
This is the test suite of the app
I have no personal AWS account, so I'm
gonna mock the boto3 library with
pytest's monkeypatching.
"""

from app import app
import pytest


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


def test_index(test_app):
    """test the index of the app"""
    response = test_app.get("/")
    assert response.status_code == 200
