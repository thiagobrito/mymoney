from django.shortcuts import redirect

from mymoney.core.models.expenses import Expenses
from mymoney.core.views.api import update_from_request


def update(request):
    return update_from_request(request, Expenses.objects.get(pk=request.POST.get('pk')))


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
