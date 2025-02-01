import json
import os

class RecordRepository:
    def __init__(self, filepath = os.path.join("frameworks", "data", "records.json")):
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

    def add_record(self, week: str, user_id: str, record: dict):
        data = self.load()
        if week not in data:
            data[week] = {}
        if user_id not in data[week]:
            data[week][user_id] = []
        data[week][user_id].append(record)
        self.save(data)

    def get_week_records(self, week: str, user_id: str):
        data = self.load()
        return data.get(week, {}).get(user_id, [])