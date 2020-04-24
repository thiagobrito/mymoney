from django.http import HttpResponse, HttpResponseNotModified
from django.shortcuts import render

from mymoney.core.services import nubank


def qrcode(request):
    nubank_worker = nubank.NubankWorker()
    request.session['uuid'] = nubank_worker.uuid

    return render(request, 'nubank/qrcode.html', context={'uuid': request.session['uuid']})


def authenticate(request):
    if nubank.authenticate(request.session['uuid'], '34026454835', 'aut55165'):
        return HttpResponse('Just processing data, you will be redirected soon...')

    return HttpResponse(status=401)


def processing(request):
    if nubank.ready(request.session['uuid']):
        return HttpResponse('processing has been complete!')

    return HttpResponseNotModified()


def summary(request):
    return render(request, 'nubank/summary.html')
