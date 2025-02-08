import datetime
from core.entities.record import Record
from utils.week_manager import get_week

class RecordWorkoutUseCase:
    def __init__(self, user_repo, record_repo):
        self.user_repo = user_repo
        self.record_repo = record_repo
    
    def execute(self, user_id: str, word: str, image: str):
        print(f"[RecordWorkoutUseCase.execute()] 실행됨 - {user_id}, {word}")
        try:
            user = self.user_repo.get_user(user_id)
            print(f"try문 실행: {user}")
            if not user:
                return False, "등록되지 않은 사용자입니다. `!등록` 명령어를 사용하여 먼저 등록을 진행해주세요!"
            if self.check_today_record(user_id):
                return False, "오늘은 이미 운동하셨습니다! 내일 또 도전합시다 💪🏻"
            if not word:
                word = "오운완 💪🏻"
                print(f"인증 진행중: {user_id}, {word}")

            current_week = get_week()
            record = Record(
                date = str(datetime.date.today()),
                word = word,
                image = image
            )
            self.record_repo.add_record(current_week, user_id, record.to_dict())
            print(f"운동 기록 저장 완료")
            return True, f"{user}님의 운동 기록이 저장되었습니다!"
        except Exception as e:
            print(f"[RecordWorkoutUseCase] 실행 중 오류 발생: {e}")
            return False, f"운동 기록 저장 중 오류가 발생했습니다."

    def check_today_record(self, user_id: str):
        try:
            current_week = get_week()
            today_date = str(datetime.date.today)
            user_records = self.record_repo.get_week_records(current_week, user_id)

            for record in user_records:
                if record["date"] == today_date:
                    return True
            return False
        except Exception as e:
            print(f"[check_today_record] 실행 중 오류 발생")
            return False