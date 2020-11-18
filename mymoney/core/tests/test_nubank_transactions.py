import unittest
from pynubank import Nubank, MockHttpClient

from mymoney.core.services.nubank_transactions import NubankTransactions


class TestNubankTransactions(unittest.TestCase):
    def setUp(self) -> None:
        self.mocked_nu = Nubank(MockHttpClient())

        self.nu_transactions = NubankTransactions(self.mocked_nu)
        self.nu_transactions.authenticate('cpf', 'password', 'uuid')

    def test_simple_transactions(self):
        transactions = list(self.nu_transactions.transactions())
        self.assertGreater(len(transactions), 0)
