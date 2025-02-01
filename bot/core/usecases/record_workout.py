import datetime
from core.entities.record import Record
from utils.week_manager import get_week

class RecordWorkoutUseCase:
    def __init__(self, user_repo, record_repo):
        self.user_repo = user_repo
        self.record_repo = record_repo
    
    def execute(self, user_id: str, word: str, image: str):
        user = self.user_repo.get_user(user_id)
        if not user:
            return False, "등록되지 않은 사용자입니다. `!등록` 명령어를 사용하여 먼저 등록을 진행해주세요!"
        if not word:
            word = "오운완 💪🏻"
        current_week = get_week()
        record = Record(
            date = str(datetime.date.today()),
            word = word,
            image = image
        )
        self.record_repo.add_record(current_week, user_id, record.to_dict())
        return True, f"{user}님의 운동 기록이 저장되었습니다!"