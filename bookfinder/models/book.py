from bookfinder.models.base import BaseModel


class Book(BaseModel):
    id = None
    title = None
    isbn = None
    author = None
