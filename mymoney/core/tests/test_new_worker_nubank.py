from django.test import TestCase

from pynubank import Nubank, MockHttpClient
from mymoney.core.services.nubank_transactions import NubankCardTransactions
from mymoney.core.services.nuconta_transactions import NuContaTransactions
from mymoney.core.services.nubank import NubankWorker


class TestNewWorkerNubank(TestCase):
    def test_simple_transactions(self):
        nubank = Nubank(MockHttpClient())
        nubank.authenticate_with_qr_code('cpf', 'pass', 'uuid')

        card_transactions = NubankCardTransactions(nubank=nubank)
        conta_transactions = NuContaTransactions(nubank=nubank, account='test_account')
        self.worker = NubankWorker('test.account.worker', card_transactions=card_transactions,
                                   conta_transactions=conta_transactions)
        self.worker.work()
