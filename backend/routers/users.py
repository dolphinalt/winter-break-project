from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from database import get_session
from models import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=list[User])
def get_users(
    session: Session = Depends(get_session),
    offset: int = 0,
):
    users = session.exec(select(User).offset(offset)).all()
    return users


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
