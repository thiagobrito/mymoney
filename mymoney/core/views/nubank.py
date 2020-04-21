from django.http import HttpResponse, HttpResponseNotModified
from pynubank import Nubank

from django.shortcuts import render


def qrcode(request):
    nu = Nubank()
    uuid, qr_code = nu.get_qr_code()

    request.session['nubank_uuid'] = uuid
    return render(request, 'nubank/qrcode.html', context={'uuid': uuid})


def authenticate(request):
    nu = Nubank()

    try:
        # nu.authenticate_with_qr_code('123456789', 'senha', request.session['nubank_uuid'])
        pass
    except:
        return HttpResponseNotModified()
    return HttpResponse('Just processing data, you will be redirected soon...')


def processing(request):
    return HttpResponse('processing has been complete!')


def summary(request):
    return render(request, 'nubank/summary.html')
