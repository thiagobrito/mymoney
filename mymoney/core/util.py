import random
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


def label_colors(number_of_colors):
    colors = ['#e74a3bbf', '#4e73dfbf', '#1cc88abf', '#36b9ccbf']
    colors += ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
    return colors[0:number_of_colors]
