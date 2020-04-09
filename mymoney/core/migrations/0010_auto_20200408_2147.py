# Generated by Django 3.0.5 on 2020-04-09 00:47

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200408_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnings',
            name='origin',
            field=models.CharField(choices=[('SL', 'Salario'), ('AG', 'AlgoMania'), ('UD', 'Udemy')], max_length=2, verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='bank_account',
            field=models.CharField(choices=[('CAI', 'Caixa'), ('SAN', 'Santander'), ('BRD', 'Bradesco'), ('NUB', 'Nubank')], max_length=3, verbose_name='bank account'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='value',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='BRL', max_digits=14, verbose_name='total value'),
        ),
        migrations.AlterField(
            model_name='funds',
            name='category',
            field=models.CharField(choices=[('OT', 'Others'), ('BO', 'Bonus'), ('AM', 'AlgoMania'), ('UD', 'Udemy'), ('SL', 'Salary')], default='', max_length=4, verbose_name='category'),
        ),
    ]
