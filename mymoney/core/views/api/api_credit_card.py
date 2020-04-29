import random
from decimal import Decimal
from datetime import datetime, timedelta

from django.db.models import Sum
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from mymoney.core.views.credit_card_estimatives import good_daily_estimate
from mymoney.core.models.credit_card import CreditCardBills
from mymoney.core.models.credit_card_updates import CreditCardCategoryUpdate
from mymoney.core import util


def burndown_chart(request, month):
    credit_card = CreditCardBills.objects.filter(payment_date__year=datetime.now().year).order_by('-transaction_time')
    credit_card = credit_card.filter(payment_date__month=month)
    if len(credit_card):
        charged_sum = credit_card.filter(charge_count__gt=1).aggregate(Sum('value'))['value__sum']

        start = util.add_months(credit_card[0].closing_date, -1)
        end = credit_card[0].closing_date

        dates = []
        expected = []
        expended = []

        good_daily_acumulated = 0
        for day in range((end - start).days):
            current = start + timedelta(days=day)
            if current == end:
                break
            dates.append('%02d/%02d' % (current.day, current.month))
            good_daily_acumulated += good_daily_estimate(credit_card, charged_sum).amount
            expected.append(good_daily_acumulated)

            month_transactions = credit_card.filter(transaction_time__lte=current).filter(charge_count=1)
            transactions_sum = month_transactions.aggregate(Sum('value'))['value__sum'] or Decimal(0)
            expended.append(transactions_sum)

        return JsonResponse(data={
            'labels': dates,
            'data1_name': 'Expected',
            'data2_name': 'Expenses',
            'data1': expected,
            'data2': expended
        })

    return HttpResponseBadRequest()


def category_chart(request, month):
    credit_card = CreditCardBills.objects.filter(payment_date__year=datetime.now().year).order_by('-transaction_time')
    credit_card = credit_card.filter(payment_date__month=month)
    report = credit_card.values('category').annotate(Sum('value')).order_by('category')

    labels = []
    data = []

    for bill in report.order_by('-value__sum'):
        labels.append(bill['category'].title())
        data.append(bill['value__sum'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'colors': util.label_colors(len(data))
    })


def update_category(request):
    if request.POST.get('name') != 'category':
        return HttpResponseBadRequest()

    try:
        obj = CreditCardCategoryUpdate.objects.get(transaction_id=request.POST.get('pk'))
        obj.category = request.POST.get('value')
        obj.save()

    except ObjectDoesNotExist:
        obj = CreditCardCategoryUpdate(transaction_id=request.POST.get('pk'),
                                       category=request.POST.get('value').lower())
        obj.save()

    for bill in CreditCardBills.objects.filter(transaction_id=request.POST.get('pk')).all():
        bill.category = request.POST.get('value').lower()
        bill.save()

    return JsonResponse(data={'status': 200})
