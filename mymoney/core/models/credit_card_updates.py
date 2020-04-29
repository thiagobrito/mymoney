from django.db import models


class CreditCardCategoryUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_id = models.TextField()
    category = models.TextField()
