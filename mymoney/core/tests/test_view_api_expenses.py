from datetime import datetime
from django.test import TestCase

from django.shortcuts import resolve_url as r

from mymoney.core.models.expenses import Expenses


class TestViewApiExpenses(TestCase):
    def test_update_request_invalid_empty_params(self):
        self.response = self.client.post(r('api.expenses.update'))
        self.assertEqual(400, self.response.status_code)

    def test_update_request_not_found_pk(self):
        self.response = self.client.post(r('api.expenses.update'), data={'pk': 123})
        self.assertEqual(404, self.response.status_code)

    def test_update_description_from_existing_expense(self):
        Expenses(pk=123, description='Old Expense', date=datetime.now().date(), value=456).save()

        self.response = self.client.post(r('api.expenses.update'), data={'pk': 123,
                                                                         'name': 'description', 'value': 'New Expense'})
        self.assertEqual(200, self.response.status_code)

        self.assertEqual('New Expense', Expenses.objects.get(pk=123).description)

    def test_update_value_from_existing_expense(self):
        Expenses(pk=123, description='Mew Expense', date=datetime.now().date(), value=111).save()

        self.response = self.client.post(r('api.expenses.update'), data={'pk': 123,
                                                                         'name': 'value', 'value': 456})
        self.assertEqual(200, self.response.status_code)

        self.assertEqual('R$456.00', str(Expenses.objects.get(pk=123).value))

    def test_scheduled_pk_not_found(self):
        self.response = self.client.get(r('api.expenses.scheduled', 123))

        self.assertEqual(404, self.response.status_code)

    def test_scheduled_valid_pk(self):
        Expenses(pk=123, description='Mew Expense', date=datetime.now().date(), value=111).save()

        self.response = self.client.get(r('api.expenses.scheduled', 123))
        self.assertEqual(200, self.response.status_code)

        self.assertTrue(Expenses.objects.get(pk=123).scheduled)

    def test_paid_pk_not_found(self):
        self.response = self.client.get(r('api.expenses.paid', 123))
        self.assertEqual(404, self.response.status_code)

    def test_paid_valid_pk(self):
        Expenses(pk=123, description='Mew Expense', date=datetime.now().date(), value=111, paid=False).save()

        self.response = self.client.get(r('api.expenses.paid', 123))
        self.assertEqual(200, self.response.status_code)

        self.assertTrue(Expenses.objects.get(pk=123).paid)

    def test_paid_should_be_scheduled_too(self):
        Expenses(pk=123, description='Mew Expense', date=datetime.now().date(), value=456, paid=False).save()

        self.response = self.client.get(r('api.expenses.paid', 123))
        self.assertEqual(200, self.response.status_code)

        self.assertTrue(Expenses.objects.get(pk=123).scheduled)

    def test_new_without_params_should_return_invalid_params(self):
        self.response = self.client.post(r('api.expenses.new'))
        self.assertEqual(400, self.response.status_code)

    def test_new_valid_values_should_update_database(self):
        self.response = self.client.post(r('api.expenses.new'), data={'date': str(datetime.now().date()),
                                                                      'description': 'testes',
                                                                      'value': 123})
        self.assertEqual(200, self.response.status_code)

    def test_recurrent_pk_not_found(self):
        self.response = self.client.get(r('api.expenses.recurrent', 123))
        self.assertEqual(404, self.response.status_code)

    def test_recurrent_found_should_update_value(self):
        Expenses(pk=123, description='Mew Expense', date=datetime.now().date(), value=789, recurrent=False).save()

        self.response = self.client.get(r('api.expenses.recurrent', 123))
        self.assertEqual(200, self.response.status_code)

        self.assertTrue(Expenses.objects.get(pk=123).recurrent)
