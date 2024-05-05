from http.client import HTTPResponse
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from mongoengine import DoesNotExist
from mongoengine.queryset import Q

from planner.models.studio import Studio
from planner.models.user import AccountType, User
from planner.routes.base_models import MemberManagerModel, PostStudio, PutStudio, StudioModel, UserBody
from planner.utils.jwt import CustomAuthJWT

router = APIRouter()


@router.get("/studio", status_code=status.HTTP_200_OK)
def get_all(authorize: CustomAuthJWT = Depends()) -> list[StudioModel]:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    studios = Studio.objects(user=subject)

    return studios


@router.post("/studio", status_code=status.HTTP_200_OK)
def create(studio: PostStudio, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    user = User.objects(email=subject).first()

    if user.type in [AccountType.FREE, AccountType.STUDIO_MEMBER]:
        raise HTTPResponse(status.HTTP_403_FORBIDDEN)

    Studio(name=studio.name, owner=user).save()


@router.put("/studio/{id}", status_code=status.HTTP_200_OK)
def put(id: str, studio: PutStudio, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    user = User.objects(email=subject).first()

    if user.type != AccountType.STUDIO:
        raise HTTPResponse(status.HTTP_403_FORBIDDEN)

    Studio.objects(pk=id).filter(Q(owner=user)).update_one(active=studio.active, name=studio.name)



@router.get("/studio/{id}", status_code=status.HTTP_200_OK)
def get(id: str, authorize: CustomAuthJWT = Depends()) -> StudioModel:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    try:
        studio = Studio.objects(pk=id, user=subject).first()
        return studio
    except DoesNotExist:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


@router.delete("/studio/{id}", status_code=status.HTTP_200_OK)
def delete_studio(id: str, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    owner = User.objects(email=subject).first()
    studio = Studio.objects(pk=id, owner=owner).first()

    if not studio:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    studio.delete()


@router.put("/studio/{id}/transfer", status_code=status.HTTP_200_OK)
def transfer_ownership(id: str, body: UserBody, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    owner = User.objects(email=subject).first()
    new_owner = User.objects(email=body.email).first()
    Studio.objects(pk=id, owner=owner).update_one(
        set__owner=new_owner,
        pull__members=new_owner,
        pull__managers=new_owner,
    )


@router.get("/studio/{id}/managers", status_code=status.HTTP_200_OK)
def get_managers(id: str, authorize: CustomAuthJWT = Depends()) -> List[MemberManagerModel]:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    studio = Studio.objects(pk=id, user=subject).first()

    return studio.managers


@router.put("/studio/{id}/manager", status_code=status.HTTP_200_OK)
def add_manager(id: str, body: UserBody, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    owner = User.objects(email=subject).first()
    manager = User.objects(email=body.email).first()
    Studio.objects(pk=id, owner=owner).update_one(add_to_set__managers=manager,pull__members=manager,
)


@router.delete("/studio/{id}/manager", status_code=status.HTTP_200_OK)
def remove_manager(id: str, body: UserBody, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    owner = User.objects(email=subject).first()
    manager = User.objects(email=body.email).first()
    Studio.objects(pk=id, owner=owner).update_one(pull__managers=manager)


@router.get("/studio/{id}/members", status_code=status.HTTP_200_OK)
def get_members(id, authorize: CustomAuthJWT = Depends()) -> List[MemberManagerModel]:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    studio = Studio.objects(pk=id, user=subject).first()

    return studio.members


@router.put("/studio/{id}/member", status_code=status.HTTP_200_OK)
def add_member(id: str, body: UserBody, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    user = User.objects(email=subject).first()
    member = User.objects(email=body.email).first()

    if user == member or member.type == AccountType.FREE:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    studios = Studio.objects(pk=id).filter(Q(owner=user)| Q(managers=user)).update_one(
        add_to_set__members=member,
        pull__managers=member,
    )
    print(studios)


@router.patch("/studio/{id}/member", status_code=status.HTTP_200_OK)
def remove_member(id: str, body: UserBody, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    user = User.objects(email=subject).first()
    member = User.objects(email=body.email).first()

    studios = Studio.objects(pk=id).filter(Q(owner=user)| Q(managers=user)).update_one(
        pull__members=member
    )
    print(studios)
