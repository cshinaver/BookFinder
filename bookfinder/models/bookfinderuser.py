from bookfinder.models.base import BaseModel


class BookfinderUser(BaseModel):
    id = None
    username = None
    email = None
    password = None
