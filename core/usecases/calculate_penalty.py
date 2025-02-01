from utils.week_manager import get_week

PENALTY_AMOUNT = 10000

class CalculatePenaltyUseCase:
    def __init__(self, user_repo, record_repo):
        self.user_repo = user_repo
        self.record_repo = record_repo

    def execute(self):
        current_week = get_week()
        users = self.user_repo.load()
        records = self.record_repo.load()
        penalty_data = {}

        for user_id, user_data in users.items():
            joined_week = user_data["joined_week"]
            total_penalty = 0

            for week, week_data in records.items():
                if week >= current_week or week < joined_week:
                    continue
                user_week_records = week_data.get(user_id, [])
                if len(user_week_records) < 3:
                    total_penalty += PENALTY_AMOUNT

            if total_penalty > 0:
                penalty_data[user_data["name"]] = total_penalty

        return penalty_data