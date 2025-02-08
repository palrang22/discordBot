from utils.time_manager import get_kst_today

def get_week():
    today = get_kst_today()
    return today.strftime("%Y-%W")
