from django.shortcuts import resolve_url as r
from django.test import TestCase


class TestViewPages(TestCase):
    def test_earnings(self):
        self.assertEqual(200, self.client.get(r('earnings')).status_code)

    def test_expenses(self):
        self.assertEqual(200, self.client.get(r('expenses')).status_code)

    def test_funds(self):
        self.assertEqual(200, self.client.get(r('funds')).status_code)
