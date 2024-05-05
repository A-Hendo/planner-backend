import pytest


@pytest.mark.db
class TestBoard:
    def test_get_board_id(self, free_client, board):
        response = free_client.get(f"/board/{board.pk}")
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == board.name

    def test_create_board_free(self, free_client):
        data = {"name": "New board"}
        response = free_client.post("/board", json=data)

        assert response.status_code == 201

    def test_cannot_get_board(self, anon_client, board):
        response = anon_client.get(f"/board/{board.pk}")

        assert response.status_code == 401

    def test_get_all(self, free_client, board):
        response = free_client.get("/board")
        data = response.json()
        print(data)

        assert response.status_code == 200
        assert len(data) == 0
