from flask.ext.login import UserMixin

from bookfinder import login_manager
from bookfinder.models.base import BaseModel


class BookfinderUser(BaseModel, UserMixin):
    id = None
    username = None
    email = None
    password = None


@login_manager.user_loader
def load_user(user_id):
    return BookfinderUser.get(user_id)
