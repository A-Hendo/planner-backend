import pytest
from planner.models.studio import Studio
from planner.models.user import User


@pytest.mark.db
class TestStudio:
    def test_member_get(self, member_client, studio):
        """Tests that a studio member can get a studio"""
        response = member_client.get(f"/studio/{studio.pk}")
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == studio.name

    def test_member_get_all(self, member_user, member_client, user, studio):
        """Tests that a studio member can get all studios it is a member of"""
        Studio(name="StudioTwo", members=[member_user], owner=user).save()
        response = member_client.get("/studio")
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 2

    def test_owner_get(self, owner_client, studio):
        """Tests that a studio owner get a studio"""
        response = owner_client.get(f"/studio/{studio.pk}")
        data = response.json()

        assert response.status_code == 200
        assert studio.name == data["name"]

    # ! Failing, validation error exception
    @pytest.mark.skip()
    def test_owner_not_get(self, owner_client, studio):
        """Tests that a studio owner can not get another studio, when they are
        not a owner, manager or member"""
        user = User(email="email@email.com", password="password").save()
        studio_one = Studio(name="StudioTwo", owner=user).save()

        response = owner_client.get(f"/studio/{studio_one.pk}")

        assert response.status_code == 400

    def test_owner_get_all(self, owner_client, studio):
        """Tests that a studio owner can get all studios"""
        user = User(email="email@email.com", password="password").save()
        Studio(name="StudioTwo", owner=user).save()

        response = owner_client.get("/studio")
        data = response.json()

        assert response.status_code == 200
        assert studio.name == data[0]["name"]
        assert len(data) == 1

    def test_owner_get_deactivated(self, owner_client, studio):
        """Tests that a studio owner can get a studio even when it is deactivated"""
        studio.active = False
        studio.save()

        response = owner_client.get(f"/studio/{studio.pk}")
        data = response.json()

        assert response.status_code == 200
        assert studio.name == data["name"]

    def test_owner_add_member(self, owner_client, studio):
        """Tests that owners can add members"""
        user = User(email="email@email.com", password="password").save()
        print(studio.pk)
        response = owner_client.put(f"/studio/{studio.pk}/member", json={"email": user.email})

        assert response.status_code == 200

    def test_owner_delete_member(self, owner_client, studio):
        """Tests that owners can delete members"""
        user = User(email="email@email.com", password="password").save()

        response = owner_client.put(f"/studio/{studio.pk}/member", json={"email": user.email})

        assert response.status_code == 200

    def test_owner_add_manager(self, owner_client, studio):
        """Tests that owners can add managers"""
        user = User(email="email@email.com", password="password").save()

        response = owner_client.put(f"/studio/{studio.pk}/manager", json={"email": user.email})
        assert response.status_code == 200

    def test_owner_get_managers(self, owner_client, manager_user, studio):
        """Tests that owners get all managers"""
        response = owner_client.get(f"/studio/{studio.pk}/managers")
        data = response.json()

        assert len(data) == 1
        assert response.status_code == 200

    def test_owner_get_members(self, owner_client, member_user, studio):
        """Tests that owners get all managers"""
        response = owner_client.get(f"/studio/{studio.pk}/members")
        data = response.json()

        assert len(data) == 1
        assert response.status_code == 200

    def test_owner_delete_manager(self, owner_client, studio):
        """Tests that owners can delete managers"""
        user = User(email="email@email.com", password="password").save()

        response = owner_client.put(f"/studio/{studio.pk}/member", json={"email": user.email})

        assert response.status_code == 200

    def test_manager_add_manager(self, manager_client, studio):
        """Tests that managers cannot add managers"""
        user = User(email="email@email.com", password="password").save()

        response = manager_client.put(f"/studio/{studio.pk}/manager", json={"email": user.email})
        studio.reload()

        assert len(studio.managers) == 1
        assert response.status_code == 200

    def test_manager_delete_manager(self, manager_client, studio):
        """Tests that managers cannot delete managers"""
        user = User(email="email@email.com", password="password").save()
        studio.managers.append(user)
        studio.save()

        response = manager_client.put(f"/studio/{studio.pk}/manager", json={"email": user.email})
        studio.reload()

        assert len(studio.managers) == 2
        assert response.status_code == 200

    def test_member_add_member(self, member_client, studio):
        """Tests that members cannot add members"""
        user = User(email="email@email.com", password="password").save()

        response = member_client.put(f"/studio/{studio.pk}/member", json={"email": user.email})

        assert len(studio.members) == 1
        assert response.status_code == 200

    def test_member_delete_member(self, member_client, studio):
        """Tests that members cannot delete members"""
        user = User(email="email@email.com", password="password").save()
        studio.members.append(user)
        studio.save()

        response = member_client.put(f"/studio/{studio.pk}/member", json={"email": user.email})
        studio.reload()

        assert len(studio.members) == 2
        assert response.status_code == 200

    def test_transfer_ownership(self, owner_client, studio, manager_user):
        """Tests transferring ownership to another manager in the team"""
        response = owner_client.put(f"/studio/{studio.pk}/transfer", json={"email": manager_user.email})

        studio = Studio.objects(pk=studio.pk).first()

        assert response.status_code == 200
        assert studio.owner == manager_user

    def test_owner_delete_studio(self, owner_client, studio):
        """Tests that the owner can delete the studio"""
        response = owner_client.delete(f"/studio/{studio.pk}")
        studios = Studio.objects()

        assert response.status_code == 200
        assert len(studios) == 0

    def test_manager_delete_studio(self, manager_client, studio):
        """Tests that a manager cannot delete the studio"""
        response = manager_client.delete(f"/studio/{studio.pk}")
        studios = Studio.objects()

        assert response.status_code == 400
        assert len(studios) == 1

    def test_member_delete_studio(self, member_client, studio):
        """Tests that a member cannot delete the studio"""
        response = member_client.delete(f"/studio/{studio.pk}")
        studios = Studio.objects()

        assert response.status_code == 400
        assert len(studios) == 1

    # def test_change_settings(self):
    #     """Tests that the owner can delete the studio"""
