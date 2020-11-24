from datetime import datetime

from django.shortcuts import resolve_url as r
from django.test import TestCase

from mymoney.core.tests import create_credit_card_bill


class BurndownChartTests(TestCase):
    def test_charged_sum_zero(self):
        create_credit_card_bill({'account': '456'})
        self.response = self.client.get(r('api.credit_card.burndown_chart', datetime.now().month))
        self.assertEqual(200, self.response.status_code)

    def test_invalid_month(self):
        self.response = self.client.get(r('api.credit_card.burndown_chart', 15))
        self.assertEqual(400, self.response.status_code)
