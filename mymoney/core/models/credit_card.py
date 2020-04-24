from django.db import models
from djmoney.models.fields import MoneyField

from mymoney.core.models.labels import Label


class CreditCardBills(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.TextField()
    transaction_id = models.TextField()
    description = models.TextField()
    labels = models.ManyToManyField(Label)
    value = MoneyField('value', max_digits=14, default_currency='BRL')
    transaction_time = models.DateTimeField()
    payment_date = models.fields.DateField()
    category = models.TextField()

    class Meta:
        verbose_name_plural = 'Credit Card Bills'
        ordering = ['transaction_time', 'value']
