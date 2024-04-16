import pytest
from planner.models.studio import Studio
from planner.models.user import User


@pytest.mark.db
class TestStudio:
    def test_get_all(self, studio):
        """Demonstrates getting all Studio objects"""
        count = len(Studio.objects())
        assert count == 1

    def test_delete(self, studio):
        """Demonstrates that studio can be deleted"""
        studio.delete()
        count = len(Studio.objects())
        assert count == 0

    # def test_assign_new_owner(self, studio, user):
    #     """Demonstrates assigning a new owner to the studio"""
    #     user_two = User(email="new@email.com", password="password").save()

    #     assert studio.owner == user
    #     assert studio.owner != user_two

    #     studio.owner = user_two
    #     studio.save()
    #     studio.reload()

    #     assert studio.owner == user_two
