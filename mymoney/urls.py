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

from mymoney.core.views.pages import index, earnings, expenses, nubank
from mymoney.core.views import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('earnings/', earnings, name='earnings'),
    path('expenses/', expenses, name='expenses'),
    path('nubank/', expenses, name='nubank'),
    path('api/v1/earnings/', api.earnings, name='api.earnings'),
    path('api/v1/sources/earnings/', api.sources_earnings, name='api.sources.earnings')
]
