from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist

from mymoney.core.models.expenses import Expenses
from mymoney.core.views.api import update_from_request

from mymoney.core.recurrences import fill_pending_recurrences


def update(request):
    pk = request.POST.get('pk')
    if pk is None:
        return HttpResponseBadRequest()

    try:
        item = Expenses.objects.get(pk=pk)
        return update_from_request(request, item)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()


def scheduled(request, pk):
    try:
        expense = Expenses.objects.get(pk=pk)
        expense.scheduled = not expense.scheduled
        expense.save()

        return JsonResponse(data={'status': 200})
    except ObjectDoesNotExist:
        return HttpResponseNotFound()


def paid(request, pk):
    try:
        expense = Expenses.objects.get(pk=pk)
        expense.paid = not expense.paid
        if expense.paid:
            expense.scheduled = True
        expense.save()

        return JsonResponse(data={'status': 200})
    except ObjectDoesNotExist:
        return HttpResponseNotFound()


def new(request):
    date = request.POST.get('date')
    description = request.POST.get('description')
    value = request.POST.get('value')

    if date is None or description is None or value is None:
        return HttpResponseBadRequest()

    Expenses(date=date, description=description, value=value).save()
    return JsonResponse(data={'status': 200})


def recurrent(request, pk):
    try:
        expense = Expenses.objects.get(pk=pk)
        expense.recurrent = not expense.recurrent
        expense.save()

        return JsonResponse(data={'status': 200})
    except ObjectDoesNotExist:
        return HttpResponseNotFound()


def fill_recurrences(request, month):
    fill_pending_recurrences(month)

    return JsonResponse(data={'status': 200})
