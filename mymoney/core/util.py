import calendar
import datetime


def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def format_money(value):
    cents = (value % 100) / 100
    total = (value - (value % 100)) / 100
    return float(total + cents)
