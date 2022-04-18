from datetime import datetime, timezone, timedelta

behind_utc = -5
cur_dt = datetime.now(tz=timezone(timedelta(hours=behind_utc)))

def cur_year():
    return cur_dt.year

def cur_month():
    return cur_dt.month

def cur_day():
    return cur_dt.day
