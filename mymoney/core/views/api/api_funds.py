from mymoney.core.models.funds import Funds
from mymoney.core.views.api import update_from_request


def update(request):
    return update_from_request(request, Funds.objects.get(pk=request.POST.get('pk')))
