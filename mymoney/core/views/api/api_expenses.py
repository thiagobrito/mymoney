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


def fill_recurrences(request, month):
    def _check_description(description):
        should_create = True
        if '(' in description and '/' in description:
            pos = description.find('(')
            description = description[:pos].strip()
            should_create = False

        return description, should_create

    year = 2020
    previous_month_expenses = Expenses.objects.filter(date__year=year, date__month=month - 1, recurrent=True)
    current_month_expenses = Expenses.objects.filter(date__year=year, date__month=month)

    for prev_expense in previous_month_expenses:
        prev_description, should_create = _check_description(prev_expense.description)

        found = False
        for curr_expense in current_month_expenses:
            curr_description, _ = _check_description(curr_expense.description)

            if curr_description == prev_description:
                curr_expense.recurrent = True
                curr_expense.save()

                found = True
                break

        if not found and should_create:
            Expenses(date=prev_expense.date.replace(month=prev_expense.date.month + 1),
                     description=prev_expense.description, value=prev_expense.value, recurrent=True).save()

    return JsonResponse(data={'status': 200})
