import pytest
from planner.models.task import Task


@pytest.mark.db
class TestTask:
    def test_owner_post(self, studio_board, owner_client):
        task = {"title": "task", "group": "Network", "description": "description"}
        response = owner_client.post(f"/task/board/{studio_board.pk}", json=task)

        assert response.status_code == 201
        assert len(Task.objects()) == 1

    def test_manager_post(self, studio_board, manager_client):
        task = {"title": "task", "group": "Network"}
        response = manager_client.post(f"/task/board/{studio_board.pk}", json=task)

        assert response.status_code == 201
        assert len(Task.objects()) == 1

    def test_member_post(self, studio_board, member_client):
        task = {"title": "task", "group": "Network"}
        response = member_client.post(f"/task/board/{studio_board.pk}", json=task)

        assert response.status_code == 201
        assert len(Task.objects()) == 1

    def test_owner_put(self, owner_client, studio_task, member_user, manager_user):
        task = {
            "title": "NewTitle",
            "type": 1,
            "description": "new description",
            "tags": [],
            "assigned": [member_user.email],
            "dependents": [manager_user.email],
            "estimation": "",
            "importance": 1,
            "time_spent": 30,
            "state": 1,
        }

        response = owner_client.put(f"/task/{studio_task.pk}", json=task)
        edited_task = Task.objects()[0]  # ? Should be studio_task.reload() but AttributeError in_bulk

        assert response.status_code == 200
        assert edited_task.title == task["title"]

    def test_manager_put(self, manager_client, studio_task, member_user, owner_user):
        task = {
            "title": "NewTitle",
            "type": 1,
            "description": "new description",
            "tags": [],
            "assigned": [member_user.email],
            "dependents": [owner_user.email],
            "estimation": "",
            "importance": 1,
            "time_spent": 30,
            "state": 1,
        }

        response = manager_client.put(f"/task/{studio_task.pk}", json=task)
        edited_task = Task.objects()[0]  # ? Should be studio_task.reload() but AttributeError in_bulk

        assert response.status_code == 200
        assert edited_task.title == task["title"]

    def test_member_put(self, member_client, studio_task, owner_user, manager_user):
        task = {
            "title": "NewTitle",
            "type": 1,
            "description": "new description",
            "tags": [],
            "assigned": [owner_user.email],
            "dependents": [manager_user.email],
            "estimation": "",
            "importance": 1,
            "time_spent": 30,
            "state": 1,
        }

        response = member_client.put(f"/task/{studio_task.pk}", json=task)
        edited_task = Task.objects()[0]  # ? Should be studio_task.reload() but AttributeError in_bulk

        assert response.status_code == 200
        assert edited_task.title == task["title"]

    def test_owner_delete(self, owner_client, studio_task):
        response = owner_client.delete(f"/task/{studio_task.pk}")
        tasks = Task.objects()

        assert response.status_code == 200
        assert len(tasks) == 0

    def test_manager_delete(self, manager_client, studio_task):
        response = manager_client.delete(f"/task/{studio_task.pk}")
        tasks = Task.objects()

        assert response.status_code == 200
        assert len(tasks) == 0

    def test_member_delete(self, member_client, studio_task):
        response = member_client.delete(f"/task/{studio_task.pk}")
        tasks = Task.objects()

        assert response.status_code == 200
        assert len(tasks) == 0

    def test_owner_get(self, owner_client, studio_task):
        response = owner_client.get(f"/task/{studio_task.pk}")
        data = response.json()
        print(data)

        assert response.status_code == 200
        assert data["title"] == studio_task.title

    def test_manager_get(self, manager_client, studio_task):
        response = manager_client.get(f"/task/{studio_task.pk}")
        data = response.json()
        print(data)

        assert response.status_code == 200
        assert data["title"] == studio_task.title

    def test_member_get(self, member_client, studio_task):
        response = member_client.get(f"/task/{studio_task.pk}")
        data = response.json()
        print(data)

        assert response.status_code == 200
        assert data["title"] == studio_task.title

    def test_owner_get_board(self, owner_client, studio_board, studio_task):
        response = owner_client.get(f"task/board/{studio_board.pk}")
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1

    def test_manager_get_board(self, manager_client, studio_board, studio_task):
        response = manager_client.get(f"task/board/{studio_board.pk}")
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1

    def test_member_get_board(self, member_client, studio_board, studio_task):
        response = member_client.get(f"task/board/{studio_board.pk}")
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1

    def test_owner_get_studio(self, owner_client, studio, studio_task):
        response = owner_client.get(f"task/studio/{studio.pk}")
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1

    def test_manager_get_studio(self, manager_client, studio, studio_task):
        response = manager_client.get(f"task/studio/{studio.pk}")
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1

    def test_member_get_studio(self, member_client, studio, studio_task):
        response = member_client.get(f"task/studio/{studio.pk}")
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
