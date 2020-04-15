from django.http import JsonResponse

from django.db.models.functions import ExtractMonth
from django.db.models import Sum

from mymoney.core.models.earnings import Earnings


def month_chart(request):
    report = Earnings.objects.annotate(month=ExtractMonth('date')) \
        .values('month') \
        .annotate(total=Sum('value')) \
        .values('month', 'total') \
        .order_by()

    months = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dec']

    start = float('inf')
    end = float('-inf')

    data = []
    for exp in report:
        start = min(start, exp['month'])
        end = max(end, exp['month'])
        data.append(exp['total'])

    labels = []
    for i in range(start, end + 1):
        labels.append(months[i])

    return JsonResponse(data={
        'labels': labels,
        'data': data}
    )


def sources_chart(request):
    report = Earnings.objects.values('origin').annotate(Sum('value')).order_by('origin')

    labels = []
    data = []

    for exp in report:
        labels.append(Earnings().source_display_name(exp['origin']))
        data.append(exp['value__sum'])

    return JsonResponse(data={
        'labels': labels,
        'data': data}
    )
