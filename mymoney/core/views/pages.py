from django.shortcuts import render
from django.db.models import Sum

from djmoney.money import Money
from mymoney.core.models.earnings import Earnings


def index(request):
    earnings = Earnings.objects.filter(date__year=2020)

    return render(request, 'index.html',
                  context={
                      'earnings': earnings,
                      'earnings_total': Money(earnings.aggregate(total=Sum('value'))['total'], currency='BRL')
                  })


def earnings(request):
    return render(request, 'earnings.html')


def expenses(request):
    return render(request, 'expenses.html')


def nubank(request):
    return render(request, 'nubank.html')
