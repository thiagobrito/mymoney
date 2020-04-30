# Generated by Django 3.0.5 on 2020-04-29 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200425_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnings',
            name='origin',
            field=models.CharField(max_length=50, verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='bank_account',
            field=models.CharField(choices=[('CAI', 'Caixa'), ('BRD', 'Bradesco'), ('NUB', 'Nubank'), ('SAN', 'Santander')], default='BRD', max_length=3, verbose_name='bank account'),
        ),
        migrations.AlterField(
            model_name='funds',
            name='category',
            field=models.CharField(choices=[('AM', 'AlgoMania'), ('UD', 'Udemy'), ('OT', 'Others'), ('SL', 'Salary'), ('BO', 'Bonus')], default='', max_length=4, verbose_name='category'),
        ),
    ]