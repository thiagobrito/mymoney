import unittest

from pynubank import Nubank, MockHttpClient
from mymoney.core.services.nubank_transactions import NubankTransactions
from mymoney.core.services.nubank import NubankWorker

from mymoney.core.models.credit_card import CreditCardBills


class TestNewWorkerNubank(unittest.TestCase):
    def setUp(self) -> None:
        nu = Nubank(MockHttpClient())
        nu.authenticate_with_qr_code('cpf', 'pass', 'uuid')

        nu_transactions = NubankTransactions(nu)
        self.worker = NubankWorker('test.account', nu_transactions)

    def test_simple_transactions(self):
        self.worker.work()

        self.assertGreater(CreditCardBills.objects.count(), 0)
