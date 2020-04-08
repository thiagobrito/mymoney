from django.contrib import admin

from mymoney.core.models.earnings import Earnings
from mymoney.core.models.funds import Funds


class EarningsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'origin', 'value', 'received')


class FundsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'value')


# Register your models here.

admin.site.register(Earnings, EarningsAdmin)
admin.site.register(Funds, FundsAdmin)
