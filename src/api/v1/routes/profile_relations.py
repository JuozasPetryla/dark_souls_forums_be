from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import get_db_session
from src.models.user_relation import UserRelation
from src.schemas.user_relation import UserRelationCreate, UserRelationResponse
from src.db.enums import UserRelationStatuses, UserRelationTypes
from src.models.user import User
from src.api.auth import get_current_user

router = APIRouter(prefix="/user-relations", tags=["User Relations"])

@router.post("/create", response_model=UserRelationResponse)
def create_relation(
    payload: UserRelationCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
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

    return relation


@router.post("/{relation_id}/accept", response_model=UserRelationResponse)
def accept_relation(
    relation_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
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


@router.post("/{relation_id}/decline", response_model=UserRelationResponse)
def decline_relation(
    relation_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
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

    relation.status = UserRelationStatuses.DECLINED
    db.commit()
    db.refresh(relation)

    return relation

@router.post("/{user_b_id}/block", response_model=UserRelationResponse)
def block_user(
    user_b_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
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
    current_user: User = Depends(get_current_user)
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
    current_user: User = Depends(get_current_user)
):
    relations = db.query(UserRelation).filter(
        (UserRelation.user_a_id == current_user.id) |
        (UserRelation.user_b_id == current_user.id)
    ).all()

    return relations
