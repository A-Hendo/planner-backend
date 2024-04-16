import pytest
from fastapi_another_jwt_auth import AuthJWT
from planner.utils.jwt import CustomAuthJWT


@pytest.mark.db()
class TestAuth:
    def test_get_access_token(self, free_client, user):
        """Demonstrates successful user login and aquires tokens"""
        response = free_client.post("/login", json={"email": user["email"], "password": "password"})
        data = response.json()

        assert response.status_code == 202
        assert "access" in data and "refresh" in data

    def test_bad_credentials(self, anon_client, user):
        """Demonstrates failed login with bad credentials"""
        response = anon_client.post("/login", json={"email": user["email"], "password": "badpassword"})
        data = response.json()

        assert response.status_code == 400
        assert "access" not in data and "refresh" not in data

    def test_no_user(self, anon_client):
        """Demonstrates failed login with bad credentials"""

        response = anon_client.post("/login", json={"email": "example@email.com", "password": "password"})
        data = response.json()

        assert response.status_code == 400
        assert "access" not in data and "refresh" not in data

    def test_get_refresh_token(self, free_client, user):
        """Demonstrates user gets new access token"""
        refresh = CustomAuthJWT().create_refresh_token(subject=user["email"])

        response = free_client.get("/refresh", headers={"Authorization": f"Bearer {refresh}"})
        data = response.json()

        assert response.status_code == 200
        assert "access" in data and "refresh" not in data

    def test_get_user_info(self, free_client, user):
        response = free_client.get("/user")
        data = response.json()

        assert response.status_code == 200
        assert data["username"] == user["username"]
        assert data["role"] == user["type"]
