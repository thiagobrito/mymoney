from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def earnings(request):
    return render(request, 'earnings.html')


def expenses(request):
    return render(request, 'expenses.html')

def nubank(request):
    return render(request, 'nubank.html')
