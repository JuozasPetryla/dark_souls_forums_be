from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.services.authentication import get_user_by_id


def delete_user_by_id(db: Session, id: int):
    user = get_user_by_id(db, id)

    if not user:
        raise HTTPException(status_code=404, detail="Such user does not exist")

    db.delete(user)
    db.commit()
