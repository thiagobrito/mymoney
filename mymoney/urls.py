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
from django.urls import path

from mymoney.core.views.pages import earnings, expenses, nubank, funds
from mymoney.core.views.api import api_earnings, api_expenses, api_funds

from mymoney.core.views import summary

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', summary.view, name='index'),
    path('summary/<int:month>/', summary.view, name='summary'),
    path('earnings/', earnings, name='earnings'),
    path('expenses/', expenses, name='expenses'),
    path('nubank/', expenses, name='nubank'),
    path('fund/', funds, name='funds'),

    path('api/v1/earnings/month_chart/', api_earnings.month_chart, name='api.earnings.month_chart'),
    path('api/v1/earnings/sources_chart/', api_earnings.sources_chart, name='api.earnings.sources_chart'),
    path('api/v1/earnings/update/', api_earnings.update, name='api.earnings.update'),

    path('api/v1/funds/update/', api_funds.update, name='api.funds.update'),

    path('api/v1/expenses/update/', api_expenses.update, name='api.expenses.update'),
    path('api/v1/expenses/scheduled/<int:pk>/', api_expenses.scheduled, name='api.expenses.scheduled'),
    path('api/v1/expenses/paid/<int:pk>/', api_expenses.paid, name='api.expenses.paid'),
]
