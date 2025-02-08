import datetime
import pytz

def get_kst_today():
    kst = pytz.timezone("Asia/Seoul")
    return datetime.datetime.now(kst).date()

