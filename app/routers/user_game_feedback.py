from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from ..backend.db_depends import get_db

from typing import Annotated

from ..models.game import Game
from ..models.user import User
from ..models.user_game_feedback import UserGameFeedback
from ..schemas import CreateFeedback, UpdateFeedback

from sqlalchemy import insert, select, update, delete

from slugify import slugify

from fastapi import APIRouter

router_feedback = APIRouter(prefix='/feedback', tags=['feedback'])


@router_feedback.get('/all_feedback')
async def all_feedback(db: Annotated[Session, Depends(get_db)]):
    feedback = db.scalars(select(UserGameFeedback)).all()
    return feedback


@router_feedback.get('/feedback_id')
async def feedback_by_id(db: Annotated[Session, Depends(get_db)], feedback_id: int):
    feedback = db.scalar(select(UserGameFeedback).where(UserGameFeedback.id == feedback_id))
    return feedback


@router_feedback.post('/create')
async def create_feedback(db: Annotated[Session, Depends(get_db)], create_feedback: CreateFeedback,
                          user_id: int, game_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FEEDBACK NOT FOUND")

    game = db.scalar(select(Game).where(Game.id == game_id))
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FEEDBACK NOT FOUND")

    existing_feedback = db.scalar(select(UserGameFeedback).where(
        UserGameFeedback.user_id == user_id,
        UserGameFeedback.game_id == game_id))
    if existing_feedback is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already left feedback for this game")

    db.execute(insert(UserGameFeedback).values(user_id=create_feedback.user_id,
                                               game_id=create_feedback.game_id,
                                               feedback_text=create_feedback.feedback_text))
    db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router_feedback.put('/update')
async def update_feedback(db: Annotated[Session, Depends(get_db)], feedback_id: int, update_feedback: UpdateFeedback):
    feedback = db.scalar(select(UserGameFeedback).where(UserGameFeedback.id == feedback_id))
    if feedback is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    db.execute(update(UserGameFeedback).where(UserGameFeedback.id == feedback_id).values(
        feedback_text=update_feedback.feedback_text
    ))

    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'rating update'}


@router_feedback.delete('/delete')
async def delete_feedback(db: Annotated[Session, Depends(get_db)], feedback_id: int):
    feedback = db.scalars(select(UserGameFeedback).where(UserGameFeedback.id == feedback_id))
    if feedback is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    db.execute(delete(UserGameFeedback).where(UserGameFeedback.id == feedback_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'rating delete'}
