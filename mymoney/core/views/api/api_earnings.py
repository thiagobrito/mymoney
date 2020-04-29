from django.http import JsonResponse

from mymoney.core.models.earnings import Earnings


def new(request):
    obj = Earnings(date=request.POST.get('date'),
                   description=request.POST.get('description'),
                   value=request.POST.get('value'),
                   origin=request.POST.get('origin'))
    obj.save()

    return JsonResponse(data={'status': 200})
