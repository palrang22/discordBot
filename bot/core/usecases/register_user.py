from core.entities.user import User
from utils.week_manager import get_week

class RegisterUserUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def execute(self, user_id: str, name: str):
        current_week = get_week()

        if self.user_repo.get_user(user_id):
            return False, f"{name}님은 이미 등록되어 있습니다."
        user = User(user_id=user_id, name=name, joined_week=current_week)
        self.user_repo.add_user(user.to_dict())
        return True, f"{name}님이 등록되었습니다! 가입 주: {current_week}"