from django.shortcuts import resolve_url as r
from django.test import TestCase


class IndexTest(TestCase):
    def test_simple_request(self):
        self.response = self.client.get(r('expenses'))
        self.assertEqual(200, self.response.status_code)
