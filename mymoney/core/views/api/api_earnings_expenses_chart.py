from datetime import datetime
from django.http import JsonResponse

from django.db.models.functions import ExtractMonth
from django.db.models import Sum

from mymoney.core.models.earnings import Earnings
from mymoney.core.models.expenses import Expenses
from mymoney.core.views.api import update_from_request


def month_chart(request):
    def _data_from_report(report):
        start = float('inf')
        end = float('-inf')

        data = []
        for exp in report:
            start = min(start, exp['month'])
            end = max(end, exp['month'])
            data.append(exp['total'])

        months = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dec']
        labels = []
        for i in range(start, end + 1):
            labels.append(months[i])

        for i in range(end, len(months)):
            data.append(0.0)

        return data, labels

    earnings = Earnings.objects.filter(date__year=datetime.now().year) \
        .annotate(month=ExtractMonth('date')) \
        .values('month') \
        .annotate(total=Sum('value')) \
        .values('month', 'total') \
        .order_by('month')
    earnings_data, labels = _data_from_report(earnings)

    expenses = Expenses.objects.filter(date__year=datetime.now().year) \
        .annotate(month=ExtractMonth('date')) \
        .values('month') \
        .annotate(total=Sum('value')) \
        .values('month', 'total') \
        .order_by('month')
    expenses_data, labels = _data_from_report(expenses)

    return JsonResponse(data={
        'labels': labels,
        'earnings': earnings_data,
        'expenses': expenses_data
    })


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


def update(request):
    return update_from_request(request, Earnings.objects.get(pk=request.POST.get('pk')))
