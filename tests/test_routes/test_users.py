import pytest


@pytest.mark.db
class TestUserModel:
    def test_create(self, anon_client):
        """Demonstrates successfully registering a user"""

        user = {
            "email": "example@email.com",
            "password": "password",
            "password_repeat": "password",
            "username": "username",
        }
        response = anon_client.post("/register", json=user)

        assert response.status_code == 201

    def test_incorrect_password(self, anon_client):
        """Demonstrates failing to register a user with incorrect password repeat"""

        user = {
            "email": "example@email.com",
            "password": "password",
            "password_repeat": "notpassword",
            "username": "username",
        }
        response = anon_client.post("/register", json=user)

        assert response.status_code == 400

    def test_incorrect_email(self, anon_client):
        """Demonstrates failing to create a user with a bad email address"""

        user = {
            "email": "user@",
            "password": "password",
            "password_repeat": "password",
            "username": "username",
        }
        response = anon_client.post("/register", json=user)

        assert response.status_code == 422
