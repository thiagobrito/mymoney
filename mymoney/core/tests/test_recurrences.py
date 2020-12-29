from django.test import TestCase

from mymoney.core.recurrences import _update_portion_payment, _check_description


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

    def test_crash_description(self):
        self.assertEqual('Carro - Kicks (Financiamento) (37/37)',
                         _update_portion_payment('Carro - Kicks (Financiamento) (36/37)'))

        self.assertEqual('TED/DOC realizado (Patrícia Gomes Dutra Brito) (Compras)',
                         _update_portion_payment('TED/DOC realizado (Patrícia Gomes Dutra Brito) (Compras)'))

    def test_check_description_simple_tests(self):
        self.assertEqual(('Teste', True), _check_description('Teste (1/10)'))

    def test_check_description_without_future_payment(self):
        self.assertEqual(('TED/DOC realizado (Patricia Gomes Dutra Brito)', False),
                         _check_description('TED/DOC realizado (Patricia Gomes Dutra Brito)'))
