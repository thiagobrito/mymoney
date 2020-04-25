from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum

from djmoney.money import Money

from mymoney.core.models.earnings import Earnings
from mymoney.core.models.funds import Funds
from mymoney.core.models.expenses import Expenses
from mymoney.core.models.credit_card import CreditCardBills


def view(request, month=None):
    earnings = Earnings.objects.filter(date__year=datetime.now().year)
    funds = Funds.objects.filter(date__year=datetime.now().year)
    expenses = Expenses.objects.filter(date__year=datetime.now().year)
    unpaid_expenses = Expenses.objects.filter(date__year=datetime.now().year)
    credit_card = CreditCardBills.objects.filter(payment_date__year=datetime.now().year)

    if month:
        earnings = earnings.filter(date__month=month)
        expenses = expenses.filter(date__month=month)
        unpaid_expenses = unpaid_expenses.filter(date__month=month)
        credit_card = credit_card.filter(payment_date__month=month)
    else:
        unpaid_expenses = unpaid_expenses.filter(date__month__lte=datetime.now().month).filter(paid=False)

    return render(request, 'index.html',
                  context={
                      'earnings': earnings,
                      'earnings_total': Money(earnings.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'funds_total': Money(funds.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'expenses': expenses,
                      'expenses_total': Money(expenses.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'unpaid_expenses': unpaid_expenses,
                      'credit_card_total': Money(credit_card.aggregate(total=Sum('value'))['total'] or 0, currency='BRL')
                  })
