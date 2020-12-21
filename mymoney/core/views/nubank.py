import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from pynubank.exception import NuRequestException

from mymoney.core.services import nubank
from mymoney.core.models.credit_card import CreditCardBills


def login(request):
    return render(request, 'nubank/login.html')


def qrcode(request):
    login = request.POST.get('login', default=None)
    password = request.POST.get('password', default=None)

    if login and password:
        request.session['uuid'] = nubank.NubankWorker(login).uuid
        request.session['login'] = login
        request.session['password'] = password

        return render(request, 'nubank/qrcode.html', context={'uuid': request.session['uuid'],
                                                              'current_month': datetime.datetime.now().month,
                                                              'current_year': datetime.datetime.now().year})

    return redirect('nubank.login')


def authenticate_and_process(request):
    uuid = request.session.get('uuid', default=None)
    login = request.session.get('login', default=None)
    password = request.session.get('password', default=None)

    if uuid and login and password:
        try:
            if request.session.get('authenticated_uuid_failed', None) != uuid:
                worker = nubank.authenticate(login, password, uuid)
                nubank.add_to_queue(uuid, worker)

                del request.session['password']
                return HttpResponse('Processing data, you will be redirected soon...')

        except NuRequestException:
            session = request.session
            session['authenticated_uuid_failed'] = uuid
            session.save()

            return HttpResponse('Failed to authenticate in Nubank (probably wrong password)...')

    return HttpResponse(status=401)


def processing(request):
    uuid = request.session.get('uuid', default=None)
    if uuid:
        return JsonResponse(nubank.status(uuid))

    return HttpResponse(status=401)


def summary(request):
    login_info = request.session.get('login', default=None)
    if login_info:
        bills = CreditCardBills.objects.filter(account=login_info).order_by('-transaction_time')
    else:
        bills = CreditCardBills.objects.all().order_by('-transaction_time')

    return render(request, 'nubank/summary.html', context={'data': bills})
