from django.db import models
from djmoney.models.fields import MoneyField


class CreditLabel(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.TextField()
    color = models.TextField()


class CreditCard(models.Model):
    id = models.AutoField(primary_key=True)
    credit_card_id = models.UUIDField()
    date = models.DateField()
    description = models.TextField()
    value = MoneyField('value', max_digits=14, default_currency='BRL')
    payment = models.fields.DateField(default=False)
    labels = models.ManyToManyField(CreditLabel)

    class Meta:
        verbose_name_plural = 'Credit Cards'
        ordering = ['date', 'value']
