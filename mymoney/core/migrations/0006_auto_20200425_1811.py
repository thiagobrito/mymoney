# Generated by Django 3.0.5 on 2020-04-25 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200424_2354'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCardSummary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=50)),
                ('monthly_goal', models.IntegerField(default=4000)),
                ('good_daily_expenses', models.IntegerField()),
                ('current_daily_expenses', models.IntegerField()),
                ('closing_day', models.IntegerField(default=19)),
                ('payment_day', models.IntegerField(default=26)),
            ],
            options={
                'verbose_name_plural': 'Credit Card Summary',
            },
        ),
        migrations.DeleteModel(
            name='CreditCardLogin',
        ),
        migrations.AlterField(
            model_name='earnings',
            name='origin',
            field=models.CharField(choices=[('SL', 'Salario'), ('UD', 'Udemy'), ('AG', 'AlgoMania')], max_length=2, verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='bank_account',
            field=models.CharField(choices=[('CAI', 'Caixa'), ('SAN', 'Santander'), ('NUB', 'Nubank'), ('BRD', 'Bradesco')], default='BRD', max_length=3, verbose_name='bank account'),
        ),
        migrations.AlterField(
            model_name='funds',
            name='category',
            field=models.CharField(choices=[('OT', 'Others'), ('BO', 'Bonus'), ('AM', 'AlgoMania'), ('UD', 'Udemy'), ('SL', 'Salary')], default='', max_length=4, verbose_name='category'),
        ),
    ]
