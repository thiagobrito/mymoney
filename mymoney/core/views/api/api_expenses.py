from django.http import JsonResponse

from mymoney.core.models.expenses import Expenses
from mymoney.core.views.api import update_from_request


def update(request):
    return update_from_request(request, Expenses.objects.get(pk=request.POST.get('pk')))


def scheduled(request, pk):
    expense = Expenses.objects.get(pk=pk)
    expense.scheduled = not expense.scheduled
    expense.save()

    return JsonResponse(data={'status': 200})


def paid(request, pk):
    expense = Expenses.objects.get(pk=pk)
    expense.paid = not expense.paid
    if expense.paid:
        expense.scheduled = True
    expense.save()

    return JsonResponse(data={'status': 200})


def new(request):
    obj = Expenses(date=request.POST.get('date'),
                   description=request.POST.get('description'),
                   value=request.POST.get('value'))
    obj.save()

    return JsonResponse(data={'status': 200})


def recurrent(request, pk):
    expense = Expenses.objects.get(pk=pk)
    expense.recurrent = not expense.recurrent
    expense.save()

    return JsonResponse(data={'status': 200})
