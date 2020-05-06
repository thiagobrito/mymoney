import datetime
from django.shortcuts import resolve_url as r
from django.test import TestCase

from mymoney.core.models.expenses import Expenses


class IndexTest(TestCase):
    def setUp(self) -> None:
        self._month = datetime.date.today().month
        self._current_date = datetime.date.today()
        self._previous_month = datetime.date.today().replace(month=datetime.date.today().month - 1)

    def test_prestacao_dont_create_new_expense(self):
        Expenses(date=self._previous_month, description='prestacao (1/10)', value=124, recurrent=True).save()
        Expenses(date=self._current_date, description='prestacao (2/18)', value=124, recurrent=False).save()

        self.response = self.client.get(r('api.expenses.fill_recurrences', month=self._month))
        self.assertEqual(200, self.response.status_code)

        self.assertEqual(2, Expenses.objects.count())

    def test_prestacao_finished_dont_create_new_expense(self):
        Expenses(date=self._previous_month, description='cortinas (5/5)', value=124, recurrent=True).save()
        Expenses(date=self._current_date, description='whatever', value=124, recurrent=False).save()

        self.response = self.client.get(r('api.expenses.fill_recurrences', month=self._month))
        self.assertEqual(200, self.response.status_code)

        self.assertEqual(2, Expenses.objects.count())

    def test_recurrent_expense_in_previous_month_should_reflect_current_month(self):
        Expenses(date=self._previous_month, description='conta de luz', value=123, recurrent=True).save()
        Expenses(date=self._current_date, description='conta de agua', value=123, recurrent=False).save()

        self.response = self.client.get(r('api.expenses.fill_recurrences', month=self._month))
        self.assertEqual(200, self.response.status_code)

        self.assertEqual(3, Expenses.objects.count())

    def test_recurrent_expense_in_previous_month_already_reflect_current_month(self):
        Expenses(date=self._previous_month, description='conta de luz', value=123, recurrent=True).save()
        Expenses(date=self._current_date, description='conta de luz', value=456, recurrent=True).save()
        Expenses(date=self._current_date, description='conta de agua', value=789, recurrent=False).save()

        self.response = self.client.get(r('api.expenses.fill_recurrences', month=self._month))
        self.assertEqual(200, self.response.status_code)

        self.assertEqual(3, Expenses.objects.count())

    def test_dont_have_any_recurrent_in_previous_month(self):
        Expenses(date=self._current_date, description='whatever', value=23, recurrent=False).save()

        self.response = self.client.get(r('api.expenses.fill_recurrences', month=self._month))
        self.assertEqual(200, self.response.status_code)

        self.assertEqual(1, Expenses.objects.count())
