class Record:
    def __init__(self, date: str, word: str, image: str):
        self.date = date
        self.word = word
        self.image = image

    def to_dict(self):
        return {
            "date": self.date,
            "word": self.word,
            "image": self.image
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Record(
            date = data["date"],
            word = data["word"],
            image = data["image"]
        )