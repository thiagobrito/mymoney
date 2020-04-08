from django.db import models
from djmoney.models.fields import MoneyField


class Earnings(models.Model):
    # 'Salario AlgoMania Udemy'

    SOURCES = {
        ('SL', 'Salario'),
        ('AG', 'AlgoMania'),
        ('UD', 'Udemy')
    }

    id = models.AutoField(primary_key=True)
    date = models.DateField()
    description = models.TextField()
    value = MoneyField('value', max_digits=14, default_currency='BRL')
    received = models.fields.BooleanField(default=False)
    origin = models.CharField('Source', max_length=2, choices=SOURCES)

    class Meta:
        verbose_name_plural = 'Earnings'
        ordering = ['date', 'value']

    @property
    def value_display(self):
        return "R$ %s" % self.value

    def source_display_name(self, source):
        return dict((k, v) for k, v in self.SOURCES)[source]
