# import pytest
# from planner.models.base_permissions import PermissionTypes
# from planner.models.user import User


# @pytest.mark.db
# class TestPermissions:
#     def test_board_owner(self, user, board):
#         permission = user.permissions().check(board)
#         assert permission == PermissionTypes.OWNER

#     def test_studio_board_owner(self, owner_user, studio_board):
#         permission = owner_user.permissions().check(studio_board)
#         assert permission == PermissionTypes.OWNER

#     def test_board_manager(self, studio_board):
#         user = User.create(email="email@email.com", password="password", username="test")
#         studio_board.studio.managers.append(user)
#         permission = user.permissions().check(studio_board)
#         assert permission == PermissionTypes.MANAGER

#     def test_board_member(self, studio_board):
#         user_one = User.create(email="email@email.com", password="password", username="test")
#         studio_board.studio.members.append(user_one)
#         studio_board.save()
#         permission = user_one.permissions().check(studio_board)
#         assert permission == PermissionTypes.MEMBER

#     def test_board_none(self, user, board):
#         user_one = User.create(email="email@email.com", password="password", username="test")
#         permission = user_one.permissions().check(board)
#         assert permission == PermissionTypes.NONE

#     def test_studio_owner(self, owner_user, studio):
#         permission = owner_user.permissions().check(studio)
#         assert permission == PermissionTypes.OWNER

#     def test_studio_manager(self, studio):
#         user = User.create(email="email@email.com", password="password", username="test")
#         studio.managers.append(user)
#         permission = user.permissions().check(studio)
#         assert permission == PermissionTypes.MANAGER

#     def test_studio_member(self, studio):
#         user = User.create(email="email@email.com", password="password", username="test")
#         studio.members.append(user)
#         permission = user.permissions().check(studio)
#         assert permission == PermissionTypes.MEMBER

#     def test_studio_none(self, studio):
#         user_one = User.create(email="email@email.com", password="password", username="test")
#         permission = user_one.permissions().check(studio)
#         assert permission == PermissionTypes.NONE
