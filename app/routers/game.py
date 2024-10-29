from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from ..backend.db_depends import get_db

from typing import Annotated

from ..models.game import Game
from ..models.user_game_feedback import UserGameFeedback
from ..models.user_game_rating import UserGameRating
from ..schemas import CreateGame, UpdateGame

from sqlalchemy import insert, select, update, delete

from slugify import slugify

from fastapi import APIRouter

router_game = APIRouter(prefix='/game', tags=['game'])


@router_game.get('/all_games')
async def all_games(db: Annotated[Session, Depends(get_db)]):
    games = db.scalars(select(Game)).all()
    return games


@router_game.get('/game_id')
async def game_by_id(db: Annotated[Session, Depends(get_db)], game_id: int):
    game = db.scalar(select(Game).where(Game.id == game_id))
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return game


@router_game.post('/create')
async def create_game(db: Annotated[Session, Depends(get_db)], create_game: CreateGame):
    db.execute(insert(Game).values(title=create_game.title,
                                   description=create_game.description,
                                   rating=create_game.rating,
                                   price=create_game.price,
                                   feedback=create_game.feedback,
                                   slug=slugify(create_game.title)))
    db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router_game.put('/update')
async def update_game(db: Annotated[Session, Depends(get_db)], game_id: int, update_game: UpdateGame):
    game = db.scalar(select(Game).where(Game.id == game_id))
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    db.execute(update(Game).where(Game.id == game_id).values(
                                   description=update_game.description,
                                   rating=update_game.rating,
                                   price=update_game.price,
                                   feedback=update_game.feedback,
                                   ))

    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'game update'}


@router_game.delete('/delete')
async def delete_game(db: Annotated[Session, Depends(get_db)], game_id: int):
    game = db.scalar(select(Game).where(Game.id == game_id))
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    db.execute(delete(Game).where(Game.id == game_id))
    db.execute(delete(UserGameFeedback).where(UserGameFeedback.game_id == game_id))
    db.execute(delete(UserGameRating).where(UserGameRating.game_id == game_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'game delete'}


@router_game.get('/game_id/rating')
async def rating_by_game_id(db: Annotated[Session, Depends(get_db)], game_id: int):
    ratings = db.scalars(select(UserGameRating).where(UserGameRating.game_id == game_id)).all()
    if ratings is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return ratings

@router_game.get('/game_id/feedback')
async def feedback_by_game_id(db: Annotated[Session, Depends(get_db)], game_id: int):
    feedbacks = db.scalars(select(UserGameFeedback).where(UserGameFeedback.game_id == game_id)).all()
    if feedbacks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return feedbacks