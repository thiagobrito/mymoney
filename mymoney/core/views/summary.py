from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum

from djmoney.money import Money

from mymoney.core.models.earnings import Earnings
from mymoney.core.models.funds import Funds
from mymoney.core.models.expenses import Expenses
from mymoney.core.models.credit_card import CreditCardBills
from mymoney.core.views.credit_card_estimatives import good_daily_estimate, month_daily_estimate
from mymoney.core.recurrences import has_pending_recurrences


def view(request, month=None, year=datetime.now().year):
    earnings = Earnings.objects.filter(date__year=year)
    funds = Funds.objects.filter(date__year=year)
    expenses = Expenses.objects.filter(date__year=year)
    unpaid_expenses = Expenses.objects.filter(date__year=year)
    credit_card = CreditCardBills.objects.filter(payment_date__year=year).order_by('-transaction_time')

    if month:
        earnings = earnings.filter(date__month=month, date__year=year)
        expenses = expenses.filter(date__month=month, date__year=year)
        unpaid_expenses = unpaid_expenses.filter(date__month=month, date__year=year)
        credit_card = credit_card.filter(payment_date__month=month, payment_date__year=year)
        charged_sum = credit_card.filter(charge_count__gt=1).aggregate(Sum('value'))['value__sum']

        credit_card_daily_estimate = good_daily_estimate(credit_card, charged_sum)
        credit_card_month_daily_expenses = month_daily_estimate(credit_card, charged_sum)
        credit_card_daily_expenses_green = credit_card_month_daily_expenses <= credit_card_daily_estimate
        pie_chart_title = 'Credit Card Categories'
        pending_recurrences = has_pending_recurrences(month, year)

        months = ['', 'January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        period_title = months[month] + ' (%s)' % year

    else:
        unpaid_expenses = unpaid_expenses.filter(date__month__lte=datetime.now().month,
                                                 date__year=datetime.now().year).filter(paid=False)
        credit_card_daily_estimate = None
        credit_card_month_daily_expenses = None
        period_title = year
        charged_sum = None
        credit_card_daily_expenses_green = False
        pie_chart_title = 'Revenue Sources'
        pending_recurrences = False

    not_recurrent = expenses.filter(recurrent=False)

    main_chart_title = 'Earnings/Expenses Overview'
    if month:
        main_chart_title = 'Credit Card Burndown Chart'

    return render(request, 'index.html',
                  context={
                      'earnings': earnings,
                      'earnings_total': Money(earnings.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'funds_total': Money(funds.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'expenses': expenses,
                      'expenses_total': Money(expenses.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'unpaid_expenses': unpaid_expenses,
                      'unpaid_expenses_total':
                          Money(unpaid_expenses.filter(paid=False).aggregate(total=Sum('value'))['total'] or 0,
                                currency='BRL'),
                      'credit_card_total': Money(credit_card.aggregate(total=Sum('value'))['total'] or 0,
                                                 currency='BRL'),
                      'period': period_title,
                      'month': month or None,
                      'credit_card_daily_estimate': credit_card_daily_estimate,
                      'credit_card_month_daily_expenses': credit_card_month_daily_expenses,
                      'credit_card': credit_card if month else None,
                      'monthly_summary': True if month else False,
                      'month_charged_sum': Money(charged_sum or 0, currency='BRL'),
                      'credit_card_daily_expenses_green': credit_card_daily_expenses_green,
                      'main_chart_title': main_chart_title,
                      'pie_chart_title': pie_chart_title,
                      'pending_recurrences': pending_recurrences,
                      'not_recurrent_total': Money(not_recurrent.aggregate(total=Sum('value'))['total'] or 0,
                                                   currency='BRL'),
                  })
