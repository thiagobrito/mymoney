from django.db import models
from djmoney.models.fields import MoneyField


class Expenses(models.Model):
    BANK_ACCOUNT = {
        ('BRD', 'Bradesco'),
        ('CAI', 'Caixa'),
        ('NUB', 'Nubank'),
        ('SAN', 'Santander')
    }

    id = models.AutoField(primary_key=True)
    date = models.DateField()
    description = models.TextField()
    value = MoneyField('total value', max_digits=14, default_currency='BRL')
    scheduled = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    bank_account = models.CharField('bank account', max_length=3, choices=BANK_ACCOUNT, default='BRD')
    transaction_id = models.CharField(max_length=50, default='')
    recurrent = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Expenses'
        ordering = ['date', 'value']

    @property
    def value_display(self):
        return self.value

