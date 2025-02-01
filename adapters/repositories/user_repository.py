import json
import os

class UserRepository:
    def __init__(self, filepath = os.path.join("frameworks", "data", "users.json")):
        self.filepath = filepath

    def load(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        
    def save(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_user(self, user_id):
        data = self.load()
        return data.get(user_id)
    
    def add_user(self, user_dict: dict):
        data = self.load()
        data[user_dict["user_id"]] = user_dict
        self.save(data)