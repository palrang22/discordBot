class User:
    def __init__(self, user_id: str, name: str, joined_week: str):
        self.user_id = user_id
        self.name = name
        self.joined_week = joined_week

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "joined_week": self.joined_week
        }
    
    @staticmethod
    def from_dict(data: dict):
        return User(
            user_id = data["user_id"],
            name = data["name"],
            joined_week = data["joined_week"]
        )