from app.modules.forgotPassword.models import Token
from core.repositories.BaseRepository import BaseRepository


class ForgotpasswordRepository(BaseRepository):
    def __init__(self):
        super().__init__(Token)
