from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models import *

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String, unique=True)
    slug = Column(String, unique=True, index=True)

    user_ratings = relationship('UserGameRating',
                                back_populates='send_to_user')
    user_feedbacks = relationship('UserGameFeedback',
                                  back_populates='send_to_user')


