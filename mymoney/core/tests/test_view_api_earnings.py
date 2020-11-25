from datetime import datetime
from django.test import TestCase

from django.shortcuts import resolve_url as r

from mymoney.core.models.earnings import Earnings


class TestViewApiEarnings(TestCase):
    def test_invalid_new_request_empty_info(self):
        self.response = self.client.post(r('api.earnings.new'))
        self.assertEqual(400, self.response.status_code)

    def test_valid_new_request_save_item(self):
        self.response = self.client.post(r('api.earnings.new'), data={'date': datetime.now().date(),
                                                                      'description': 'Test Earnings',
                                                                      'value': 123, 'origin': 'Unit Tests'})
        self.assertEqual(200, self.response.status_code)

        self.assertEqual(1, Earnings.objects.count())
