import pytest
from planner.models.task import Task
from planner.models.user import User


@pytest.mark.db
class TestTasks:
    def test_get_all(self, task):
        count = len(Task.objects())
        assert count == 1

    def test_delete(self, task):
        count = len(Task.objects())
        assert count == 1

        task.delete()

        count = len(Task.objects())
        assert count == 0

    # def test_add_assigned(self, task):
    #     assert len(task.assigned) == 0
    #     user_one = User(email="new@email.com", password="password")
    #     user_two = User(email="new2@email.com", password="password")

    #     task.assigned.append(user_one)
    #     task.assigned.append(user_two)
    #     task.save()
    #     task.reload()

    #     assert len(task.assigned) == 2
