from mymoney.core.models.expenses import Expenses
from mymoney.core.models.earnings import Earnings

from mymoney.core.util import str_to_datetime, format_money, format_money_from_description


class NuContaTransactions:
    def __init__(self, account, nubank=None):
        self._nubank = nubank
        self._account = account

    def load_all_transactions(self):
        return self.load(self._nubank.get_account_statements())

    def load(self, transactions):
        functions = {'TransferOutEvent': self._transfer_out_event,
                     'TransferOutReversalEvent': self._transfer_out_reversal_event,
                     'TransferInEvent': self._transfer_in_event,
                     'DebitPurchaseEvent': self._debit_event,
                     'BillPaymentEvent': self._bill_payment_event,
                     'DebitPurchaseReversalEvent': self._debit_reversal_event,
                     'BarcodePaymentEvent': self._barcode_payment_event,
                     'DebitWithdrawalFeeEvent': self._debit_withdrawalfee_event,
                     'DebitWithdrawalEvent': self._debit_withdrawal_event}

        for transaction in transactions:
            functions[transaction['__typename']](transaction, self._account)

    @staticmethod
    def _transfer_in_event(transaction, account):
        if Earnings.objects.filter(transaction_id=transaction['id']).count() == 0:
            Earnings.objects.create(transaction_id=transaction['id'],
                                    description='TED/DOC recebido (%s)' % transaction['originAccount']['name'],
                                    date=str_to_datetime(transaction['postDate']), value=transaction['amount'],
                                    received=True, origin='Nubank')

    @staticmethod
    def _transfer_out_reversal_event(transaction, account):
        if Earnings.objects.filter(transaction_id=transaction['id']).count() == 0:
            name = transaction['detail'].split('-')[0].strip()
            amount = transaction.get('amount', format_money_from_description(transaction['detail']))

            Earnings.objects.create(transaction_id=transaction['id'],
                                    date=str_to_datetime(transaction['postDate']),
                                    description='TED/DOC devolvido (%s)' % name,
                                    value=amount, received=True, origin='Nubank')

    @staticmethod
    def _debit_reversal_event(transaction, account):
        if Earnings.objects.filter(transaction_id=transaction['id']).count() == 0:
            amount = transaction.get('amount', format_money_from_description(transaction['detail']))

            Earnings.objects.create(transaction_id=transaction['id'],
                                    date=str_to_datetime(transaction['postDate']),
                                    description='Estorno de debito (%s)' % transaction['detail'],
                                    value=amount, received=True, origin='Nubank')

    @staticmethod
    def _transfer_out_event(transaction, account):
        if Expenses.objects.filter(transaction_id=transaction['id']).count() == 0:
            Expenses.objects.create(transaction_id=transaction['id'],
                                    date=str_to_datetime(transaction['postDate']),
                                    description='TED/DOC realizado (%s)' % (
                                        transaction['destinationAccount']['name']
                                    ),
                                    value=transaction['amount'],
                                    scheduled=True, paid=True, bank_account='NUB')

    @staticmethod
    def _debit_event(transaction, account):
        if Expenses.objects.filter(transaction_id=transaction['id']).count() == 0:
            title = transaction['detail'].split('-')[0].strip()

            Expenses.objects.create(transaction_id=transaction['id'],
                                    date=str_to_datetime(transaction['postDate']),
                                    description='Compra no Debito (%s)' % title, value=transaction['amount'],
                                    scheduled=True, paid=True, bank_account='NUB')

    @staticmethod
    def _bill_payment_event(transaction, account):
        if Expenses.objects.filter(transaction_id=transaction['id']).count() == 0:
            amount = format_money_from_description(transaction['detail'])

            transaction_date = str_to_datetime(transaction['postDate'])
            Expenses.objects.create(transaction_id=transaction['id'],
                                    date=transaction_date, description='Pagamento da fatura', value=amount,
                                    scheduled=True, paid=True, bank_account='NUB')

            Expenses.objects.filter(transaction_id=account, date__month=transaction_date.month).delete()

    @staticmethod
    def _barcode_payment_event(transaction, account):
        if Expenses.objects.filter(transaction_id=transaction['id']).count() == 0:
            Expenses.objects.create(transaction_id=transaction['id'],
                                    date=str_to_datetime(transaction['postDate']),
                                    description='Pagamento de Boleto',
                                    value=transaction['amount'],
                                    scheduled=True, paid=True, bank_account='NUB')

    @staticmethod
    def _debit_withdrawalfee_event(transaction, account):
        if Expenses.objects.filter(transaction_id=transaction['id']).count() == 0:
            location = transaction['detail'].split('-')[0].strip()

            Expenses.objects.create(transaction_id=transaction['id'],
                                    date=str_to_datetime(transaction['postDate']),
                                    description='Tarifa de Saque (%s)' % location,
                                    value=transaction['amount'],
                                    scheduled=True, paid=True, bank_account='NUB')

    @staticmethod
    def _debit_withdrawal_event(transaction, account):
        if Expenses.objects.filter(transaction_id=transaction['id']).count() == 0:
            location = transaction['detail'].split('-')[0].strip()

            Expenses.objects.create(transaction_id=transaction['id'],
                                    date=str_to_datetime(transaction['postDate']),
                                    description='Saque (%s)' % location, value=transaction['amount'],
                                    scheduled=True, paid=True, bank_account='NUB')
