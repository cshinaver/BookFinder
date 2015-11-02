from flask.ext.login import UserMixin

from bookfinder import login_manager
from bookfinder.models.base import BaseModel


class BookfinderUser(BaseModel, UserMixin):
    id = None
    username = None
    email = None
    pw_hash = None

    def __init__(self, username=None, password=None):
        self.username = username
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return BookfinderUser.get(user_id)
