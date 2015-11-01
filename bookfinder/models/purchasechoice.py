from bookfinder.models.base import BaseModel


class PurchaseChoice(BaseModel):
    id = None
    price = None
    type = None
    isRental = None
    link = None
    seller = None
    book_id = None
