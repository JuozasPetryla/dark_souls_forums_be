from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.session import get_db_session
from src.db.models import User, UserRelation
from src.schemas.user_relations import UserRelationCreate, UserRelationResponse
from src.db.enums import UserRelationStatuses, UserRelationTypes
from src.services.authentication import get_user_by_token
from src.services.email import send_friend_request_email


router = APIRouter()


@router.post("/create", response_model=UserRelationResponse)
async def create_relation(
    payload: UserRelationCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_user_by_token)
):
    if current_user.id == payload.user_b_id:
        raise HTTPException(400, "Cannot create a relation with yourself")

    existing = db.query(UserRelation).filter(
        ((UserRelation.user_a_id == current_user.id) &
         (UserRelation.user_b_id == payload.user_b_id)) |
        ((UserRelation.user_a_id == payload.user_b_id) &
         (UserRelation.user_b_id == current_user.id))
    ).first()

    if existing:
        raise HTTPException(400, "Relation already exists")

    relation = UserRelation(
        user_a_id=current_user.id,
        user_b_id=payload.user_b_id,
        type=payload.type,
        status=(
            UserRelationStatuses.PENDING
            if payload.type == UserRelationTypes.FRIEND
            else UserRelationStatuses.ACCEPTED
        )
    )

    db.add(relation)
    db.commit()
    db.refresh(relation)

    if relation.type == UserRelationTypes.FRIEND and relation.status == UserRelationStatuses.PENDING:
        target_user = db.query(User).filter(User.id == payload.user_b_id).first()
        if target_user and target_user.email:
            await send_friend_request_email(target_user.email, current_user.nickname), 

    return relation

@router.post("/{relation_id}/accept", response_model=UserRelationResponse)
def accept_relation(
    relation_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_user_by_token)
):
    relation = db.query(UserRelation).filter(
        UserRelation.id == relation_id,
        UserRelation.type == UserRelationTypes.FRIEND,
        UserRelation.status == UserRelationStatuses.PENDING
    ).first()

    if not relation:
        raise HTTPException(404, "Friend request not found")

    if relation.user_b_id != current_user.id:
        raise HTTPException(403, "You cannot accept this request")

    relation.status = UserRelationStatuses.ACCEPTED
    db.commit()
    db.refresh(relation)

    return relation


@router.post("/{relation_id}/decline")
def decline_relation(
    relation_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_user_by_token)
):
    relation = db.query(UserRelation).filter(
        UserRelation.id == relation_id,
        UserRelation.type == UserRelationTypes.FRIEND,
        UserRelation.status == UserRelationStatuses.PENDING
    ).first()

    if not relation:
        raise HTTPException(404, "Friend request not found")

    if relation.user_b_id != current_user.id:
        raise HTTPException(403, "You cannot decline this request")

    db.delete(relation)
    db.commit()

    return {"success": True}


@router.post("/{user_b_id}/block", response_model=UserRelationResponse)
def block_user(
    user_b_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_user_by_token)
):
    if current_user.id == user_b_id:
        raise HTTPException(400, "Cannot block yourself")

    existing = db.query(UserRelation).filter(
        ((UserRelation.user_a_id == current_user.id) &
         (UserRelation.user_b_id == user_b_id)) |
        ((UserRelation.user_a_id == user_b_id) &
         (UserRelation.user_b_id == current_user.id))
    ).first()

    if existing:
        db.delete(existing)
        db.commit()

    relation = UserRelation(
        user_a_id=current_user.id,
        user_b_id=user_b_id,
        type=UserRelationTypes.BLOCKED,
        status=UserRelationStatuses.ACCEPTED
    )

    db.add(relation)
    db.commit()
    db.refresh(relation)

    return relation


@router.delete("/{relation_id}")
def delete_relation(
    relation_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_user_by_token)
):
    relation = db.query(UserRelation).filter(UserRelation.id == relation_id).first()

    if not relation:
        raise HTTPException(404, "Relation not found")

    if current_user.id not in (relation.user_a_id, relation.user_b_id):
        raise HTTPException(403, "You cannot delete this relationship")

    db.delete(relation)
    db.commit()

    return {"message": "Relation deleted successfully"}


@router.get("/list", response_model=list[UserRelationResponse])
def list_relations(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_user_by_token)
):
    relations = db.query(UserRelation).filter(
        (UserRelation.user_a_id == current_user.id) |
        (UserRelation.user_b_id == current_user.id)
    ).all()

    return relations

@router.get("/status/{user_b_id}")
def relation_status(
    user_b_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_user_by_token)
):
    relation = db.query(UserRelation).filter(
        ((UserRelation.user_a_id == current_user.id) &
         (UserRelation.user_b_id == user_b_id)) |
        ((UserRelation.user_a_id == user_b_id) &
         (UserRelation.user_b_id == current_user.id))
    ).first()

    if not relation:
        return {"relation_exists": False}

    return {
        "relation_exists": True,
        "id": relation.id,
        "type": relation.type.value,
        "status": relation.status.value,
        "initiator": (
            "me" if relation.user_a_id == current_user.id else "other"
        )
    }

