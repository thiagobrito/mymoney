from django.contrib import admin

from mymoney.core.models.earnings import Earnings


class EarningsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'origin', 'value', 'received')


# Register your models here.

admin.site.register(Earnings, EarningsAdmin)
