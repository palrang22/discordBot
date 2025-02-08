from utils.week_manager import get_week

class GetStatusUseCase:
    def __init__(self, user_repo, record_repo):
        self.user_repo = user_repo
        self.record_repo = record_repo

    def execute(self):
        print("GetStatusUseCase.execute() 호출됨")
        current_week = get_week()
        users = self.user_repo.load()
        print(f"로드된 사용자 수: {len(users)}")
        status = {}
        for user_id, user_data in users.items():
            print(f"GetStatusUseCase for문 돌아가는중: {user_id}, {user_data['name']}")
            records = self.record_repo.get_week_records(current_week, user_id)
            status[user_id] = {
                "name": user_data["name"],
                "records": records,
                "count": len(records)
            }
        return status