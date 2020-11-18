"""mymoney URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from mymoney.core.views.pages import earnings, expenses, nubank, funds
from mymoney.core.views.api import api_earnings_expenses_chart, api_expenses, api_funds, api_credit_card, api_earnings
from mymoney.core.views import nubank

from mymoney.core.views import summary

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),

    path('', summary.view, name='index'),
    path('summary/<int:month>/<int:year>', summary.view, name='summary'),
    path('earnings/', earnings, name='earnings'),
    path('expenses/', expenses, name='expenses'),
    path('fund/', funds, name='funds'),

    path('nubank/login/', nubank.login, name='nubank.login'),
    path('nubank/qrcode/', nubank.qrcode, name='nubank.qrcode'),
    path('nubank/authenticate/', nubank.authenticate_and_process, name='nubank.authenticate'),
    path('nubank/processing/', nubank.processing, name='nubank.processing'),
    path('nubank/summary/', nubank.summary, name='nubank.summary'),

    path('api/v1/credit_card/burndown/<int:month>/', api_credit_card.burndown_chart,
         name='api.credit_card.burndown_chart'),
    path('api/v1/credit_card/category/<int:month>/', api_credit_card.category_chart,
         name='api.credit_card.category_chart'),
    path('api/v1/credit_card/update_category/', api_credit_card.update_category,
         name='api.credit_card.update_category'),
    path('api/v1/credit_card/update_payment_date/', api_credit_card.update_payment_date,
         name='api.credit_card.update_payment_date'),

    path('api/v1/earnings/month_chart/', api_earnings_expenses_chart.month_chart, name='api.earnings.month_chart'),
    path('api/v1/earnings/sources_chart/', api_earnings_expenses_chart.sources_chart,
         name='api.earnings.sources_chart'),
    path('api/v1/earnings/update/', api_earnings_expenses_chart.update, name='api.earnings.update'),
    path('api/v1/earnings/new/', api_earnings.new, name='api.earnings.new'),

    path('api/v1/funds/update/', api_funds.update, name='api.funds.update'),

    path('api/v1/expenses/update/', api_expenses.update, name='api.expenses.update'),
    path('api/v1/expenses/scheduled/<int:pk>/', api_expenses.scheduled, name='api.expenses.scheduled'),
    path('api/v1/expenses/paid/<int:pk>/', api_expenses.paid, name='api.expenses.paid'),
    path('api/v1/expenses/recurrent/<int:pk>/', api_expenses.recurrent, name='api.expenses.recurrent'),
    path('api/v1/expenses/fill_recurrences/<int:month>/', api_expenses.fill_recurrences,
         name='api.expenses.fill_recurrences'),
    path('api/v1/new/', api_expenses.new, name='api.expenses.new'),
]
