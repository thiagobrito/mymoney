from datetime import datetime
from django.db.models import Sum

from djmoney.money import Money

from mymoney.core import util


def good_daily_estimate(credit_card, month_charged_sum):
    if credit_card:
        goals = {2021: {1: 5000, 2: 5000, 3: 4500, 4: 4500, 5: 4000, 6: 4000,
                        7: 4000, 8: 4000, 9: 4000, 10: 4000, 11: 4000, 12: 4000}}
        goal = goals[credit_card[0].closing_date.year][credit_card[0].closing_date.month]

        start = util.add_months(credit_card[0].closing_date, -1)
        end = credit_card[0].closing_date

        number_of_days = (end - start).days
        if goal >= month_charged_sum:
            return Money((goal - month_charged_sum) / number_of_days, currency='BRL')
    return Money(0, currency='BRL')


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
