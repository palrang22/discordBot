from adapters.repositories.db_connection import get_db_connection

class UserRepository:
    def __init__(self):
        self.conn = get_db_connection()
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close
        self.conn.close

    def get_user(self, user_id):
        query = """
        SELECT user_id, name, joined_week
        FROM users
        WHERE user_id = %s
        """
        self.cur.execute(query, (user_id,))
        result = self.cur.fetchone()
        if result:
            return {"user_id": result[0], "name": result[1], "joined_week": result[2]}
        return None
    
    def add_user(self, user_data):
        query = """
        INSERT INTO users (user_id, name, joined_week)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING;
        """
        self.cur.execute(query, (user_data["user_id"], user_data["name"], user_data["joined_week"]))
        self.conn.commit()