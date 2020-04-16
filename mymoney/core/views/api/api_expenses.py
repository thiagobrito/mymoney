from django.shortcuts import redirect
from django.http import JsonResponse
from djmoney.money import Money

from mymoney.core.models.expenses import Expenses


def update(request):
    expense = Expenses.objects.get(pk=request.POST.get('pk'))
    value = request.POST.get('value', default=None)
    if value:
        name = request.POST.get('name', default=None)
        if name == 'description':
            expense.description = value
        elif name == 'value':
            expense.value = Money(value.replace('R$', ''), currency='BRL')
        expense.save()

    return JsonResponse(data={'msg': 'success'})


def scheduled(request, pk):
    expense = Expenses.objects.get(pk=pk)
    expense.scheduled = not expense.scheduled
    expense.save()

    return redirect('/expenses/')


def paid(request, pk):
    expense = Expenses.objects.get(pk=pk)
    expense.paid = not expense.paid
    if expense.paid:
        expense.scheduled = True
    expense.save()

    return redirect('/expenses/')
