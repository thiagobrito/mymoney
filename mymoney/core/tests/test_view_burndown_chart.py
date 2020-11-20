from django.shortcuts import resolve_url as r
from django.test import TestCase

'''
class IndexTest(TestCase):
    def setUp(self):
        fill_database()

    def test_simple_request(self):
        self.response = self.client.get(r('api.credit_card.burndown_chart', 5))
        self.assertEqual(200, self.response.status_code)

    def test_invalid_month(self):
        self.response = self.client.get(r('api.credit_card.burndown_chart', 15))
        self.assertEqual(400, self.response.status_code)
'''