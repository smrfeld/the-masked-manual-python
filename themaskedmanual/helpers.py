from datetime import date, datetime

def date_to_str(timestamp: date) -> str:
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def str_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')