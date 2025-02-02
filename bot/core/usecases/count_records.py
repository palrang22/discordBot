from utils.week_manager import get_week

class CountRecordsUseCase:
    def __init__(self, record_repo):
        self.record_repo = record_repo

    def execute(self, user_id: str) -> int:
        current_week = get_week()
        records = self.record_repo.load()
        user_records = records.get(current_week, {}).get(user_id, [])
        return(len(user_records))