import datetime

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
    closing_date = models.fields.DateField(default=datetime.datetime.now, blank=True)
    category = models.TextField()
    charge_count = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Credit Card Bills'
        ordering = ['transaction_time', 'value']

