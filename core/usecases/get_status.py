from utils.week_manager import get_week

class GetStatusUseCase:
    def __init__(self, user_repo, record_repo):
        self.user_repo = user_repo
        self.record_repo = record_repo

    def execute(self):
        current_week = get_week()
        users = self.user_repo.load()
        status = {}
        for user_id, user_data in users.items():
            records = self.record_repo.get_week_records(current_week, user_id)
            status[user_id] = {
                "name": user_data["name"],
                "records": records
            }
        return status