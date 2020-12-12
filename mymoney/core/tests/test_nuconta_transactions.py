from django.test import TestCase
from pynubank import Nubank, MockHttpClient
from mymoney.core.tests.data import account_statements

from mymoney.core.models.expenses import Expenses
from mymoney.core.models.earnings import Earnings

from mymoney.core.services.nuconta_transactions import NuContaTransactions


class TestNubankTransactions(TestCase):
    def setUp(self) -> None:
        self.mocked_nu = Nubank(MockHttpClient())
        self.mocked_nu.authenticate_with_qr_code('34026454835', 'Aut55165??', 'uuid')

        self.nu_conta = NuContaTransactions()

    def test_process_transactions_TransferOutEvent_save_as_expense(self):
        self.nu_conta.load([account_statements.transactions[0]])

        expense = Expenses.objects.all()[0]

        self.assertEqual(1, Expenses.objects.count())
        self.assertEqual('TED/DOC realizado (Waldecir Ruiz Acrani)', expense.description)
        self.assertEqual('R$470.00', str(expense.value))
        self.assertTrue(expense.scheduled)
        self.assertTrue(expense.paid)

    def test_process_transactions_TransferInEvent_save_as_earning(self):
        self.nu_conta.load([account_statements.transactions[1]])

        earning = Earnings.objects.all()[0]

        self.assertEqual(1, Earnings.objects.count())
        self.assertEqual('TED/DOC recebido (Carlos Augusto Galhiego Vieira)', earning.description)
        self.assertEqual('R$60.88', str(earning.value))
        self.assertTrue(earning.received)
        self.assertEqual('Nubank', earning.origin)

    def test_process_transactions_DebitPurchaseEvent_save_as_expense(self):
        transaction = [{
            "id": "5fbed412-10dd-4e6a-9d6e-9d3583b89126",
            "__typename": "DebitPurchaseEvent",
            "title": "Compra no débito",
            "detail": "Mineirin do Queijo Iii - R$ 56,00",
            "postDate": "2020-11-25",
            "amount": 56.0
        }]
        self.nu_conta.load(transaction)

        expense = Expenses.objects.first()

        self.assertEqual(1, Expenses.objects.count())
        self.assertEqual('Compra no Debito (Mineirin do Queijo Iii)', expense.description)
        self.assertEqual('R$56.00', str(expense.value))
        self.assertTrue(expense.scheduled)
        self.assertTrue(expense.paid)

    def test_process_transactions_BillPaymentEvent_save_as_expense(self):
        transaction = [{
            "id": "5fb59b58-2eaa-459d-9c22-f6d0546b5c64",
            "__typename": "BillPaymentEvent",
            "title": "Pagamento da fatura",
            "detail": "Cartão Nubank - R$ 100,00",
            "postDate": "2020-11-18",
            "amount": None
        }]
        self.nu_conta.load(transaction)

        expense = Expenses.objects.first()

        self.assertEqual(1, Expenses.objects.count())
        self.assertEqual('Pagamento da fatura', expense.description)
        self.assertEqual('R$100.00', str(expense.value))
        self.assertTrue(expense.scheduled)
        self.assertTrue(expense.paid)

    def test_process_transactions_TransferOutReversalEvent_save_as_earning(self):
        transaction = [{
            "id": "5f351895-4079-4539-890f-cc60d852468a",
            "__typename": "TransferOutReversalEvent",
            "title": "Transferência devolvida",
            "detail": "José Luís Alves Da Silva - R$ 2.857,00",
            "postDate": "2020-08-13",
            "amount": 2857.0
        }]

        self.nu_conta.load(transaction)

        earning = Earnings.objects.all()[0]

        self.assertEqual(1, Earnings.objects.count())
        self.assertEqual('TED/DOC devolvido (José Luís Alves Da Silva)', earning.description)
        self.assertEqual('R$2,857.00', str(earning.value))
        self.assertTrue(earning.received)
        self.assertEqual('Nubank', earning.origin)
