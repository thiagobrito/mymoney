import unittest
from pynubank import Nubank, MockHttpClient

from mymoney.core.services.nubank_transactions import NubankTransactions


class TestNubankTransactions(unittest.TestCase):
    def setUp(self) -> None:
        self.mocked_nu = Nubank(MockHttpClient())

        self.nu_transactions = NubankTransactions(self.mocked_nu)
        self.nu_transactions.authenticate('cpf', 'password', 'uuid')
