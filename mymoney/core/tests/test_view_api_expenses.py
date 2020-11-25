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
