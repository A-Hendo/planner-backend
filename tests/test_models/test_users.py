import pytest
from planner.models.board import Board
from planner.models.studio import Studio
from planner.models.task import Task
from planner.models.user import User


@pytest.mark.db
class TestUserModel:
    def test_get_all(self, user):
        """Tests getting all users"""
        users = User.objects()
        assert len(users) == 1

    def test_delete(self, user):
        """Tests a user is deleted"""
        user.delete()
        count = len(User.objects())
        assert count == 0

    def test_delete_board(self, user, board):
        """Tests when the user/owner is deleted the board is deleted too"""
        user.delete()

        count = len(User.objects())
        assert count == 0

        count = len(Board.objects())
        assert count == 0

    def test_delete_other(self, user, board):
        """Tests when a user is not an owner or member and is deleted that the board is not deleted"""
        user_two = User.create(email="this@email.com", password="asdasdds", username="user")
        user_two.delete()

        count = len(Board.objects())
        assert count == 1

    def test_delete_studio_member(self, user, studio_board, studio):
        """Tests when a user is a studio member and is deleted that the board is not deleted"""
        user_two = User.create(email="this@email.com", password="asdasdds", username="user")
        studio.members.append(user_two)
        user_two.delete()

        count = len(Board.objects())
        assert count == 1

        count = len(Studio.objects())
        assert count == 1

    def test_delete_studio_member_task(self, user, studio_board, studio, task):
        """Tests when a user is a studio member and is deleted that the task is not deleted"""
        user_two = User.create(email="this@email.com", password="asdasdds", username="user")
        studio.members.append(user_two)
        user_two.delete()

        count = len(Task.objects())
        assert count == 1

    def test_delete_owner_studio_board(self, owner_user, studio_board):
        """Tests when a user is a studio owner and is deleted that the board is as well"""
        owner_user.delete()

        count = len(Board.objects())
        assert count == 0

    def test_delete_owner_studio(self, owner_user, studio):
        """Tests when a user is a studio owner and is deleted that the studio is as well"""
        owner_user.delete()

        count = len(Studio.objects())
        assert count == 0

    def test_delete_owner_studio_task(self, owner_user, studio_task):
        """Tests when a user is a studio owner and is deleted that the task is as well"""
        owner_user.delete()

        count = len(Task.objects())
        assert count == 0

    def test_update_settings(self, user):
        pass
