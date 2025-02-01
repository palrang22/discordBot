import datetime

def get_week():
    today = datetime.date.today()
    return today.strftime("%Y-%W")