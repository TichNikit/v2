class Game(Base):
    __tablename__ = 'games'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    rating = Column(Integer)
    price = Column(Float)
    feedback = Column(String)
    slug = Column(String, unique=True, index=True)

    game_ratings = relationship('UserGameRating',
                                back_populates='send_to_game')
    game_feedbacks = relationship('UserGameFeedback',
                                  back_populates='send_to_game')

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)
    slug = Column(String, unique=True, index=True)

    user_ratings = relationship('UserGameRating',
                                back_populates='send_to_user')
    user_feedbacks = relationship('UserGameFeedback',
                                  back_populates='send_to_user')

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

class UserGameRating(Base):
    __tablename__ = 'user_game_ratings'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    rating_int = Column(Integer) # я так понял, тут мы и напишем оценку

    send_to_game = relationship('Game',
                               back_populates='game_ratings')
    send_to_user = relationship('User',
                                back_populates='user_ratings')


@app.post("/register")
async def reg_user(request: Request, db: Annotated[Session, Depends(get_db)], username: str = Form(...),
                      firstname: str = Form(...), lastname: str = Form(...), password: str = Form(...)) -> HTMLResponse:
    user = db.scalar(select(User).where(User.username == username))
    if user:
        return HTMLResponse(f'Логин уже занят((( Попробуйте другой', status_code=400)
    db.execute(insert(User).values(username=username,
                                   firstname=firstname,
                                   lastname=lastname,
                                   password=password,
                                   slug=slugify(username)))
    db.commit()
    user_id = db.scalar(select(User.id).where(User.username == username))
    return templates.TemplateResponse('welcome_user.html', {"request": request, "username": username,
                                                            'user_id': user_id})