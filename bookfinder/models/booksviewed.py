from datetime import datetime

from bookfinder.models.base import BaseModel


class BooksViewed(BaseModel):
    id = None
    book_id = None
    user_id = None
    time_added = datetime.now()
