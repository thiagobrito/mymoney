from django.test import TestCase

from mymoney.core.recurrences import _update_portion_payment


class RecurrencesTests(TestCase):
    def test_update_portion_payment(self):
        self.assertEqual('Teste (2/10)', _update_portion_payment('Teste (1/10)'))
        self.assertEqual('Teste (3/10)', _update_portion_payment('Teste (2/10)'))
        self.assertEqual('Teste (4/10)', _update_portion_payment('Teste (3/10)'))
        self.assertEqual('Teste (5/10)', _update_portion_payment('Teste (4/10)'))
        self.assertEqual('Teste (6/10)', _update_portion_payment('Teste (5/10)'))
        self.assertEqual('Teste (7/10)', _update_portion_payment('Teste (6/10)'))
        self.assertEqual('Teste (10/10)', _update_portion_payment('Teste (9/10)'))
        self.assertEqual('Teste (11/20)', _update_portion_payment('Teste (10/20)'))
