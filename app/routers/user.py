from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from ..backend.db_depends import get_db

from typing import Annotated

from ..models.user import User
from ..models.user_game_feedback import UserGameFeedback
from ..models.user_game_rating import UserGameRating
from ..schemas import CreateUser, UpdateUser

from sqlalchemy import insert, select, update, delete

from slugify import slugify

from fastapi import APIRouter

router_user = APIRouter(prefix='/user', tags=['user'])


@router_user.get('/all_users')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router_user.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    return user


@router_user.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   password=create_user.password,
                                   slug=slugify(create_user.username)))
    db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router_user.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    db.execute(update(User).where(User.id == user_id).values(
        firstname=update_user.firstname,
        lastname=update_user.lastname,
    ))

    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'user update'}


@router_user.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(UserGameFeedback).where(UserGameFeedback.user_id == user_id))
    db.execute(delete(UserGameRating).where(UserGameRating.user_id == user_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'user delete'}


@router_user.get('/user_id/rating')
async def rating_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    ratings = db.scalars(select(UserGameRating).where(UserGameRating.user_id == user_id)).all()
    if ratings is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return ratings

@router_user.get('/user_id/feedback')
async def feedback_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    feedbacks = db.scalars(select(UserGameFeedback).where(UserGameFeedback.user_id == user_id)).all()
    if feedbacks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return feedbacks