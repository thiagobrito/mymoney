from colorfield.fields import ColorField
from django.db import models


class Label(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.TextField()
    color = ColorField(default='#FF0000')
