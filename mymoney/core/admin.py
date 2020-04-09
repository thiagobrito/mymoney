from django.contrib import admin
from django import forms

from dateutil.relativedelta import relativedelta

from mymoney.core.models.earnings import Earnings
from mymoney.core.models.funds import Funds
from mymoney.core.models.expenses import Expenses


class EarningsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'origin', 'value', 'received')


class FundsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'value')


class ExpensesForm(forms.ModelForm):
    # custom field not backed by database
    number_of_payments = forms.IntegerField(initial=1, min_value=1)

    class Meta:
        model = Expenses
        fields = '__all__'


class ExpensesAdmin(admin.ModelAdmin):
    form = ExpensesForm
    list_display = ('date', 'description', 'value', 'scheduled', 'paid', 'bank_account')

    def save_model(self, request, obj, form, change):
        number_of_payments = int(form.data['number_of_payments'])
        if number_of_payments == 1:
            obj.save()
        else:
            for payment in range(0, number_of_payments):
                date = obj.date + relativedelta(months=+payment)
                description = obj.description + ' (%d/%d)' % (payment + 1, number_of_payments)
                value = obj.value / number_of_payments

                Expenses.objects.create(
                    date=date,
                    description=description,
                    value=value.amount,
                    scheduled=True,
                    paid=False,
                    bank_account=obj.bank_account
                )


# Register your models here.

admin.site.register(Earnings, EarningsAdmin)
admin.site.register(Funds, FundsAdmin)
admin.site.register(Expenses, ExpensesAdmin)
