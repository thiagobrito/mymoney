from django.shortcuts import resolve_url as r
from django.test import TestCase


class TestViewSummary(TestCase):
    def test_summary(self):
        self.assertEqual(200, self.client.get(r('summary', month=1, year=2020)).status_code)
