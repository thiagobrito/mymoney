# Generated by Django 3.0.7 on 2020-12-21 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201214_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcarddateupdate',
            name='orig_transaction_time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='bank_account',
            field=models.CharField(choices=[('CAI', 'Caixa'), ('NUB', 'Nubank'), ('SAN', 'Santander'), ('BRD', 'Bradesco')], default='BRD', max_length=3, verbose_name='bank account'),
        ),
        migrations.AlterField(
            model_name='funds',
            name='category',
            field=models.CharField(choices=[('BO', 'Bonus'), ('AM', 'AlgoMania'), ('OT', 'Others'), ('SL', 'Salary'), ('UD', 'Udemy')], default='', max_length=4, verbose_name='category'),
        ),
    ]
