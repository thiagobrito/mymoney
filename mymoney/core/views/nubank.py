from django.http import HttpResponse, HttpResponseNotModified
from django.shortcuts import render, redirect

from mymoney.core.services import nubank
from mymoney.core.models.credit_card import CreditCardBills


def login(request):
    return render(request, 'nubank/login.html')


def qrcode(request):
    login = request.POST.get('login', default=None)
    password = request.POST.get('password', default=None)

    if login and password:
        request.session['uuid'] = nubank.NubankWorker().uuid
        request.session['login'] = login
        request.session['password'] = password

        return render(request, 'nubank/qrcode.html', context={'uuid': request.session['uuid']})

    return redirect('nubank.login')


def authenticate(request):
    uuid = request.session.get('uuid', default=None)
    login = request.session.get('login', default=None)
    password = request.session.get('password', default=None)

    if uuid and login and password:
        if nubank.authenticate(uuid, login, password):
            del request.session['password']

            return HttpResponse('Processing data, you will be redirected soon...')

    return HttpResponse(status=401)


def processing(request):
    if nubank.ready(request.session['uuid']):
        return HttpResponse('processing has been complete!')

    return HttpResponseNotModified()


def summary(request):
    login = request.session.get('login', default=None)
    if login:
        bills = CreditCardBills.objects.filter(account=login)
    else:
        bills = CreditCardBills.objects.all()

    return render(request, 'nubank/summary.html', context={'data': bills})
