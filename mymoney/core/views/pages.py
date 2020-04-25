from django.shortcuts import render

from mymoney.core.models.earnings import Earnings
from mymoney.core.models.funds import Funds
from mymoney.core.models.expenses import Expenses


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
