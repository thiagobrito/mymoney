import datetime

from django.db import models


class CreditCardCategoryUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_id = models.TextField()
    category = models.TextField()


class CreditCardDateUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_id = models.TextField()
    orig_transaction_time = models.DateField()
    orig_payment_date = models.DateField(default=datetime.datetime.now, blank=True)
    new_payment_date = models.DateField()
    new_closing_date = models.DateField()
    refunded = models.BooleanField(default=False)
