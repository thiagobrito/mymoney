from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum

from djmoney.money import Money
from mymoney.core.models.earnings import Earnings
from mymoney.core.models.funds import Funds
from mymoney.core.models.expenses import Expenses


def index(request):
    earnings = Earnings.objects.filter(date__year=2020)
    funds = Funds.objects.filter(date__year=2020)
    expenses = Expenses.objects.filter(date__year=2020)

    unpaid_expenses = Expenses.objects.filter(date__year=2020, date__month__lte=datetime.now().month).filter(paid=False)

    return render(request, 'index.html',
                  context={
                      'earnings': earnings,
                      'earnings_total': Money(earnings.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'funds_total': Money(funds.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'expenses': expenses,
                      'expenses_total': Money(expenses.aggregate(total=Sum('value'))['total'] or 0, currency='BRL'),
                      'unpaid_expenses': unpaid_expenses
                  })


def earnings(request):
    earnings = Earnings.objects.filter(date__year=2020).order_by('-date')

    return render(request, 'earnings.html',
                  context={'earnings': earnings})


def expenses(request):
    expenses = Expenses.objects.filter(date__year=2020).order_by('-date')

    return render(request, 'expenses.html',
                  context={'expenses': expenses})


def nubank(request):
    return render(request, 'nubank.html')


def funds(request):
    funds = Funds.objects.filter(date__year=2020).order_by('-date')

    return render(request, 'funds.html',
                  context={
                      'funds': funds
                  })
