from django.http import HttpResponseBadRequest, JsonResponse

from mymoney.core.models.earnings import Earnings


def new(request):
    date = request.POST.get('date')
    description = request.POST.get('description')
    value = request.POST.get('value')
    origin = request.POST.get('origin')

    if date is None or description is None or value is None or origin is None:
        return HttpResponseBadRequest()

    Earnings(date=date, description=description, value=value, origin=origin).save()

    return JsonResponse(data={'status': 200})
