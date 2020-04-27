from datetime import datetime
from calendar import monthrange
from django.shortcuts import render
from django.db.models import Sum

from djmoney.money import Money

from mymoney.core.models.earnings import Earnings
from mymoney.core.models.funds import Funds
from mymoney.core.models.expenses import Expenses
from mymoney.core.models.credit_card import CreditCardBills
from mymoney.core import util


def view(request, month=None):
    def _credit_card_good_daily_estimate(credit_card, month_charged_sum, goal=4000):
        start = util.add_months(credit_card[0].closing_date, -1)
        end = credit_card[0].closing_date

        number_of_days = (end - start).days
        if goal < month_charged_sum:
            return Money(0, currency='BRL')
        return Money((goal - month_charged_sum) / number_of_days, currency='BRL')

    def _credit_card_month_daily_estimate(credit_card, month_charged_sum):
        total_sum = credit_card.aggregate(Sum('value'))['value__sum']
        if total_sum:
            start = util.add_months(credit_card[0].closing_date, -1)
            end = credit_card[0].closing_date

            if start <= datetime.now().date() <= end:
                end = datetime.now().date()

            number_of_days = (end - start).days
            return Money((total_sum - month_charged_sum) / number_of_days, currency='BRL')

        return Money(0, currency='BRL')

    year = datetime.now().year
    earnings = Earnings.objects.filter(date__year=year)
    funds = Funds.objects.filter(date__year=year)
    expenses = Expenses.objects.filter(date__year=year)
    unpaid_expenses = Expenses.objects.filter(date__year=year)
    credit_card = CreditCardBills.objects.filter(payment_date__year=year).order_by('-transaction_time')

    if month:
        earnings = earnings.filter(date__month=month)
        expenses = expenses.filter(date__month=month)
        unpaid_expenses = unpaid_expenses.filter(date__month=month)
        credit_card = credit_card.filter(payment_date__month=month)
        charged_sum = credit_card.filter(charge_count__gt=1).aggregate(Sum('value'))['value__sum']

        credit_card_daily_estimate = _credit_card_good_daily_estimate(credit_card, charged_sum)
        credit_card_month_daily_expenses = _credit_card_month_daily_estimate(credit_card, charged_sum)
        credit_card_daily_expenses_green = credit_card_month_daily_expenses <= credit_card_daily_estimate

        months = ['', 'January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        period = months[month] + ' (%s)' % year

    else:
        unpaid_expenses = unpaid_expenses.filter(date__month__lte=datetime.now().month).filter(paid=False)
        credit_card_daily_estimate = None
        credit_card_month_daily_expenses = None
        period = year
        charged_sum = None
        credit_card_daily_expenses_green = False

    return render(request, 'index.html',
                  context={
                      'earnings': earnings,
                      'earnings_total': Money(earnings.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'funds_total': Money(funds.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'expenses': expenses,
                      'expenses_total': Money(expenses.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'unpaid_expenses': unpaid_expenses,
                      'credit_card_total': Money(credit_card.aggregate(total=Sum('value'))['total'] or 0,
                                                 currency='BRL'),
                      'period': period,
                      'credit_card_daily_estimate': credit_card_daily_estimate,
                      'credit_card_month_daily_expenses': credit_card_month_daily_expenses,
                      'credit_card': credit_card if month else None,
                      'monthly_summary': True if month else False,
                      'month_charged_sum': Money(charged_sum or 0, currency='BRL'),
                      'credit_card_daily_expenses_green': credit_card_daily_expenses_green,
                  })
