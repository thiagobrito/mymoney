from django.http import JsonResponse

from mymoney.core.models.expenses import Expenses


def update(request):
    return JsonResponse(data={'msg': 'success'})

