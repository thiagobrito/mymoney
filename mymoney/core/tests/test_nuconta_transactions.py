from django.test import TestCase
from pynubank import Nubank, MockHttpClient

from mymoney.core.models.expenses import Expenses
from mymoney.core.models.earnings import Earnings

from mymoney.core.util import str_to_datetime
from mymoney.core.services.nuconta_transactions import NuContaTransactions


class TestNubankTransactions(TestCase):
    def setUp(self) -> None:
        self.mocked_nu = Nubank(MockHttpClient())
        self.mocked_nu.authenticate_with_qr_code('34026454835', 'Aut55165??', 'uuid')

        self.nu_conta = NuContaTransactions(account='test.account')

    def test_process_transactions_TransferOutEvent_save_as_expense(self):
        transaction = [{
            'id': '5fd39bfe-e8ba-4450-a0c3-4393a6a53887', '__typename': 'TransferOutEvent',
            'title': 'Transferência enviada', 'detail': 'Waldecir Ruiz Acrani - R$\xa0470,00',
            'postDate': '2020-12-11', 'amount': 470.0,
            'destinationAccount': {'name': 'Waldecir Ruiz Acrani'}
        }]
        self.nu_conta.load(transaction)

        expense = Expenses.objects.all()[0]

        self.assertEqual(1, Expenses.objects.count())
        self.assertEqual('TED/DOC realizado (Waldecir Ruiz Acrani)', expense.description)
        self.assertEqual('R$470.00', str(expense.value))
        self.assertEqual('NUB', expense.bank_account)
        self.assertTrue(expense.scheduled)
        self.assertTrue(expense.paid)

    def test_process_transactions_TransferInEvent_save_as_earning(self):
        transaction = [{
            'id': '5fd2519e-62a6-498c-8924-e6d5a4178457',
            '__typename': 'TransferInEvent',
            'title': 'Transferência recebida',
            'detail': 'R$ 60,88',
            'postDate': '2020-12-10',
            'amount': 60.88,
            'originAccount': {'name': 'Carlos Augusto Galhiego Vieira'}
        }]
        self.nu_conta.load(transaction)

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
        self.assertEqual('NUB', expense.bank_account)
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
        self.assertEqual('Pagamento da fatura (test.account)', expense.description)
        self.assertEqual('R$100.00', str(expense.value))
        self.assertEqual('NUB', expense.bank_account)
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

    def test_process_transactions_DebitPurchaseReversalEvent_save_as_earning(self):
        transaction = [{'id': '5fa6baf4-f2c4-4fe8-816e-073c96f38284',
                        '__typename': 'DebitPurchaseReversalEvent',
                        'title': 'Estorno de dÃ©bito',
                        'detail': 'Spoleto - R$ 55,00',
                        'postDate': '2020-11-07'}]

        self.nu_conta.load(transaction)

        earning = Earnings.objects.first()

        self.assertEqual(1, Earnings.objects.count())
        self.assertEqual('Estorno de debito (Spoleto - R$ 55,00)', earning.description)
        self.assertEqual('R$55.00', str(earning.value))
        self.assertTrue(earning.received)
        self.assertEqual('Nubank', earning.origin)

    def test_process_transactions_BarcodePaymentEvent_save_as_expense(self):
        transaction = [{"id": "5f6cab82-8377-4f0f-a586-78df2e14cc8b",
                        "__typename": "BarcodePaymentEvent",
                        "title": "Pagamento efetuado",
                        "detail": "Pagamento Boleto",
                        "postDate": "2020-09-24",
                        "amount": 100.0}]

        self.nu_conta.load(transaction)

        expense = Expenses.objects.first()

        self.assertEqual(1, Expenses.objects.count())
        self.assertEqual('Pagamento de Boleto', expense.description)
        self.assertEqual('R$100.00', str(expense.value))
        self.assertEqual('NUB', expense.bank_account)
        self.assertTrue(expense.scheduled)
        self.assertTrue(expense.paid)

    def test_process_transactions_DebitWithdrawalFeeEvent_save_as_expense(self):
        transaction = [{"id": "5e5a77c4-992f-4183-a120-dd64334233e6",
                        "__typename": "DebitWithdrawalFeeEvent",
                        "title": "Tarifa de saque",
                        "detail": "Padaria Jardins - R$ 6,50",
                        "postDate": "2020-02-29",
                        "amount": 6.5}]

        self.nu_conta.load(transaction)

        expense = Expenses.objects.first()

        self.assertEqual(1, Expenses.objects.count())
        self.assertEqual('Tarifa de Saque (Padaria Jardins)', expense.description)
        self.assertEqual('R$6.50', str(expense.value))
        self.assertEqual('NUB', expense.bank_account)
        self.assertTrue(expense.scheduled)
        self.assertTrue(expense.paid)

    def test_process_transactions_DebitWithdrawalEvent_save_as_expense(self):
        transaction = [{"id": "5e5a77c4-5974-49cd-a121-961d338a1395",
                        "__typename": "DebitWithdrawalEvent",
                        "title": "Saque",
                        "detail": "Padaria Jardins - R$ 100,00",
                        "postDate": "2020-02-29",
                        "amount": 100.0}]

        self.nu_conta.load(transaction)

        expense = Expenses.objects.first()

        self.assertEqual(1, Expenses.objects.count())
        self.assertEqual('Saque (Padaria Jardins)', expense.description)
        self.assertEqual('R$100.00', str(expense.value))
        self.assertEqual('NUB', expense.bank_account)
        self.assertTrue(expense.scheduled)
        self.assertTrue(expense.paid)
