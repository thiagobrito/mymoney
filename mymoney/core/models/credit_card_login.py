from django.db import models


class CreditCardLogin(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Credit Card Login'
