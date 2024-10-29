from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from app.models import *


class Game(Base):
    __tablename__ = 'games'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    rating = Column(Integer)
    price = Column(Float)
    feedback = Column(String)
    slug = Column(String, unique=True, index=True)

    game_ratings = relationship('UserGameRating',
                                back_populates='send_to_game')
    game_feedbacks = relationship('UserGameFeedback',
                                  back_populates='send_to_game')

