from utils.week_manager import get_week

PENALTY_AMOUNT = 10000

class CalculatePenaltyUseCase:
    def __init__(self, user_repo, record_repo):
        self.user_repo = user_repo
        self.record_repo = record_repo

    def execute(self):
        print(f"CalculatePenaltyUseCase.execute() 호출됨")
        current_week = get_week()
        print(f"현재 주: {current_week}")
        users = self.user_repo.load()
        records = self.record_repo.load()
        print(f"DB 확인: {users[0]}, {records[0]}")
        penalty_data = {}

        for user_id, user_data in users.items():
            print(f"사용자 확인: {user_id}, {user_data[0]}")
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