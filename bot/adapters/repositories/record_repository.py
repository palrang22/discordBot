from adapters.repositories.db_connection import get_db_connection

class RecordRepository:
    def __init__(self):
        print("[RecordRepository] 연결 시도중...")
        try:
            self.conn = get_db_connection()
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"[RecordRepository] 연결 실패: {e}")

    def load(self):
        query = """
        SELECT user_id, week, date, word, image FROM records
        """
        try:
            self.cur.execute(query)
            results = self.cur.fetchall()

            records = {}
            for row in results:
                records[row[0]] = {"week": row[1], "date": row[2], "word": row[3], "image": row[4]}
            return records
        except Exception as e:
            print(f"[load] 데이터 불러오기 실패: {e}")
            return {}

    def add_record(self, week: str, user_id: str, record_data: dict):
        query = """
        INSERT INTO records (user_id, week, date, word, image)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            print(f"[add_record] 입력 데이터: {user_id}, {week}, {record_data['word']}")
            self.cur.execute(query, (user_id, week, record_data["date"], record_data["word"], record_data["image"]))
            self.conn.commit()
            print("[add_record] 데이터 추가 성공!")
        except Exception as e:
            print(f"[add_record] 데이터 추가 실패: {e}")

    def get_week_records(self, week: str, user_id: str):
        query = """
        SELECT date, word, image
        FROM records
        WHERE week = %s AND user_id = %s
        """
        try:
            print(f"[get_week_records] 조회 데이터: {user_id}, {week}")
            self.cur.execute(query, (week, user_id))
            results = self.cur.fetchall()
            print(f"[get_week_records] 조회 결과 개수: {len(results)}")
            return [{"date": row[0], "word": row[1], "image": row[2]} for row in results]
        except Exception as e:
            print(f"[get_week_records] 데이터 조회 실패: {e}")
        
    def close(self):
        print("[RecordRepository] DB 연결 종료")
        self.cur.close()
        self.conn.close()