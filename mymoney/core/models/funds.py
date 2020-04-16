from django.db import models
from djmoney.models.fields import MoneyField


class Funds(models.Model):
    CATEGORY = {
        ('SL', 'Salary'),
        ('BO', 'Bonus'),
        ('AM', 'AlgoMania'),
        ('UD', 'Udemy'),
        ('OT', 'Others'),
    }

    id = models.AutoField(primary_key=True)
    date = models.DateField()
    description = models.TextField()
    value = MoneyField('value', max_digits=14, default_currency='BRL')
    category = models.CharField('category', max_length=4, choices=CATEGORY, default='')

    class Meta:
        verbose_name_plural = 'Funds'
        ordering = ['date', 'value']

    @property
    def value_display(self):
        return self.value
