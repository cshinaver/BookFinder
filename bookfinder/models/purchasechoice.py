from bookfinder.models.base import BaseModel


class PurchaseChoice(BaseModel):
    id = None
    price = None
    type = None
    isRental = None
    link = None
    local_seller_id = None
    isLocalSeller = None
    remoteSellerName = None
    book_id = None
