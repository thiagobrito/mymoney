from datetime import datetime
from django.db.models import Sum

from djmoney.money import Money

from mymoney.core import util


def good_daily_estimate(credit_card, month_charged_sum, goal=4000):
    start = util.add_months(credit_card[0].closing_date, -1)
    end = credit_card[0].closing_date

    number_of_days = (end - start).days
    if goal < month_charged_sum:
        return Money(0, currency='BRL')
    return Money((goal - month_charged_sum) / number_of_days, currency='BRL')


def month_daily_estimate(credit_card, month_charged_sum):
    total_sum = credit_card.aggregate(Sum('value'))['value__sum']
    if total_sum:
        start = util.add_months(credit_card[0].closing_date, -1)
        end = credit_card[0].closing_date

        if start <= datetime.now().date() <= end:
            end = datetime.now().date()

        number_of_days = (end - start).days or 1
        return Money((total_sum - month_charged_sum) / number_of_days, currency='BRL')

    return Money(0, currency='BRL')
