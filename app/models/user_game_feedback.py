from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models import *


class UserGameFeedback(Base):
    __tablename__ = 'user_game_feedback'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    feedback_text = Column(String)

    send_to_game = relationship('Game',
                                back_populates='game_feedbacks')
    send_to_user = relationship('User',
                                back_populates='user_feedbacks')