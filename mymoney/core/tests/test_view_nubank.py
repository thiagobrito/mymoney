from django.shortcuts import resolve_url as r
from django.test import TestCase


class IndexTest(TestCase):
    def test_nubank_summary_page(self):
        self.response = self.client.get(r('nubank.summary'))
        self.assertEqual(200, self.response.status_code)
