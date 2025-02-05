from adapters.repositories.db_connection import get_db_connection

class RecordRepository:
    def __init__(self):
        self.conn = get_db_connection()
        self.cur = self.conn.cursor()

    def add_record(self, week: str, user_id: str, record_data: dict):
        query = """
        INSERT INTO records (user_id, week, date, word, image)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cur.execute(query, (user_id, week, record_data["date"], record_data["word"], record_data["image"]))
        self.conn.commit()

    def get_week_records(self, week: str, user_id: str):
        query = """
        SELECT date, word, image
        FROM records
        WHERE week = %s AND user_id = %s
        """
        self.cur.execute(query, (week, user_id))
        results = self.cur.fetchall()
        return [{"date": row[0], "word": row[1], "image": row[2]} for row in results]
    
    def close(self):
        self.cur.close()
        self.conn.close()