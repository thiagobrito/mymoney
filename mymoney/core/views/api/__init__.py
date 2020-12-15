from django.http import JsonResponse
from djmoney.money import Money


def update_from_request(request, object):
    value = request.POST.get('value', default=None)
    if value:
        name = request.POST.get('name', default=None)
        if name == 'description':
            object.description = value
        elif name == 'value':
            object.value = Money(value.replace('R$', '').replace(',', ''), currency='BRL')

        if object.value.amount == 0:
            object.delete()
        else:
            object.save()

    return JsonResponse(data={'msg': 'success'})
