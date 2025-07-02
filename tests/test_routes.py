import pytest


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_signup_page(client):
    response = client.get("/signup")
    assert response.status_code == 200


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_feedback_page(client):
    response = client.get("/feedback")
    assert response.status_code == 302


def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302


if __name__ == "__main__":
    pytest.main(["-v", __file__])
