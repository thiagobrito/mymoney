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


# TODO:
# Achar uma maneira melhor de calcular o daily estimate
# - Pegar a data do primeiro dia da fatura atual do cartão (close date)
# - Calcular numero de dias, estes dias nao é do mes... e sim a diff do open date ate o close date

def view(request, month=None):
    def _credit_card_good_daily_estimate(credit_card, month, year, goal=6000):
        charged_sum = credit_card.filter(charge_count__gt=1).aggregate(Sum('value'))['value__sum']

        number_of_days = monthrange(year, month)[1]
        return Money((goal - charged_sum) / number_of_days, currency='BRL')

    def _credit_card_month_daily_estimate(credit_card):
        total_sum = credit_card.aggregate(Sum('value'))['value__sum']
        if total_sum:
            start = credit_card[0].closing_date
            end = util.add_months(credit_card[0].closing_date, 1)

            if start >= datetime.now().date() <= end:
                end = datetime.now().date()

            number_of_days = (end - start).days

            charged_sum = credit_card.filter(charge_count__gt=1).aggregate(Sum('value'))['value__sum']
            return Money((total_sum - charged_sum) / number_of_days, currency='BRL')

        return Money(0, currency='BRL')

    year = datetime.now().year
    earnings = Earnings.objects.filter(date__year=year)
    funds = Funds.objects.filter(date__year=year)
    expenses = Expenses.objects.filter(date__year=year)
    unpaid_expenses = Expenses.objects.filter(date__year=year)
    credit_card = CreditCardBills.objects.filter(payment_date__year=year)

    if month:
        earnings = earnings.filter(date__month=month)
        expenses = expenses.filter(date__month=month)
        unpaid_expenses = unpaid_expenses.filter(date__month=month)
        credit_card = credit_card.filter(payment_date__month=month)
        credit_card_daily_estimate = _credit_card_good_daily_estimate(credit_card, month, year)
        credit_card_month_daily_expenses = _credit_card_month_daily_estimate(credit_card)

        months = ['', 'January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        period = months[month] + ' (%s)' % year

    else:
        unpaid_expenses = unpaid_expenses.filter(date__month__lte=datetime.now().month).filter(paid=False)
        credit_card_daily_estimate = None
        credit_card_month_daily_expenses = None
        period = year

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
                      'credit_card_month_daily_expenses': credit_card_month_daily_expenses
                  })
