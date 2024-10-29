from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    password: str


class UpdateUser(BaseModel):
    firstname: str
    lastname: str

#_____________________________________________________________________________
class CreateGame(BaseModel):
    title: str
    description: str
    rating: int
    price: float
    feedback: str


class UpdateGame(BaseModel):
    description: str
    rating: int
    price: float
    feedback: str

#_____________________________________________________________________________
class CreateRating(BaseModel):
    user_id: int
    game_id: int
    rating_int: int

class UpdateRating(BaseModel):
    rating_int: int

#________________________________________________________________________________
class CreateFeedback(BaseModel):
    user_id: int
    game_id: int
    feedback_text: str

class UpdateFeedback(BaseModel):
    feedback_text: str