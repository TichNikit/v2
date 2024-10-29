from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from ..backend.db_depends import get_db

from typing import Annotated

from ..models.game import Game
from ..models.user import User
from ..models.user_game_rating import UserGameRating
from ..schemas import CreateRating, UpdateRating

from sqlalchemy import insert, select, update, delete

from slugify import slugify

from fastapi import APIRouter

router_rating = APIRouter(prefix='/rating', tags=['rating'])


@router_rating.get('/all_rating')
async def all_rating(db: Annotated[Session, Depends(get_db)]):
    ratings = db.scalars(select(UserGameRating)).all()
    return ratings


@router_rating.get('/rating_id')
async def rating_by_id(db: Annotated[Session, Depends(get_db)], rating_id: int):
    rating = db.scalar(select(UserGameRating).where(UserGameRating.id == rating_id))
    return rating


@router_rating.post('/create')
async def create_rating(db: Annotated[Session, Depends(get_db)], create_rating: CreateRating,
                        user_id: int, game_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RATING NOT FOUND")

    game = db.scalar(select(Game).where(Game.id == game_id))
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RATING NOT FOUND")

    existing_rating = db.scalar(select(UserGameRating).where(
        UserGameRating.user_id == user_id,
        UserGameRating.game_id == game_id))
    if UserGameRating is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already left rating for this game")

    db.execute(insert(UserGameRating).values(user_id=create_rating.user_id,
                                             game_id=create_rating.game_id,
                                             rating_int=create_rating.rating_int))
    db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router_rating.put('/update')
async def update_rating(db: Annotated[Session, Depends(get_db)], rating_id: int, update_rating: UpdateRating):
    rating = db.scalar(select(UserGameRating).where(UserGameRating.id == rating_id))
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    db.execute(update(UserGameRating).where(UserGameRating.id == rating_id).values(
        rating_int=update_rating.rating_int
    ))

    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'rating update'}


@router_rating.delete('/delete')
async def delete_rating(db: Annotated[Session, Depends(get_db)], rating_id: int):
    rating = db.scalars(select(UserGameRating).where(UserGameRating.id == rating_id))
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    db.execute(delete(UserGameRating).where(UserGameRating.id == rating_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'rating delete'}
