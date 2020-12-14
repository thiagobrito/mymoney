from mymoney.core.models.expenses import Expenses
from mymoney.core.models.earnings import Earnings

from mymoney.core.util import str_to_datetime, format_money, format_money_from_description


class NuContaTransactions:
    def __init__(self, nubank=None):
        self._nubank = nubank

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
            functions[transaction['__typename']](transaction)

    @staticmethod
    def _transfer_out_event(transaction):
        expense = Expenses.objects.create(date=str_to_datetime(transaction['postDate']),
                                          description='TED/DOC realizado (%s)' % (
                                              transaction['destinationAccount']['name']
                                          ),
                                          value=transaction['amount'], scheduled=True, paid=True,
                                          bank_account='Nubank')
        expense.save()

    @staticmethod
    def _transfer_in_event(transaction):
        earning = Earnings.objects.create(date=str_to_datetime(transaction['postDate']),
                                          description='TED/DOC recebido (%s)' % (
                                              transaction['originAccount']['name']
                                          ),
                                          value=transaction['amount'], received=True, origin='Nubank')
        earning.save()

    @staticmethod
    def _debit_event(transaction):
        title = transaction['detail'].split('-')[0].strip()

        expense = Expenses.objects.create(date=str_to_datetime(transaction['postDate']),
                                          description='Compra no Debito (%s)' % title,
                                          value=transaction['amount'], scheduled=True, paid=True,
                                          bank_account='Nubank')
        expense.save()

    @staticmethod
    def _bill_payment_event(transaction):
        amount = format_money_from_description(transaction['detail'])

        expense = Expenses.objects.create(date=str_to_datetime(transaction['postDate']),
                                          description='Pagamento da fatura', value=amount, scheduled=True, paid=True,
                                          bank_account='Nubank')
        expense.save()

    @staticmethod
    def _transfer_out_reversal_event(transaction):
        name = transaction['detail'].split('-')[0].strip()
        amount = transaction.get('amount', format_money_from_description(transaction['detail']))

        earning = Earnings.objects.create(date=str_to_datetime(transaction['postDate']),
                                          description='TED/DOC devolvido (%s)' % name,
                                          value=amount, received=True, origin='Nubank')
        earning.save()

    @staticmethod
    def _debit_reversal_event(transaction):
        amount = transaction.get('amount', format_money_from_description(transaction['detail']))

        earning = Earnings.objects.create(date=str_to_datetime(transaction['postDate']),
                                          description='Estorno de debito (%s)' % transaction['detail'],
                                          value=amount, received=True, origin='Nubank')
        earning.save()

    @staticmethod
    def _barcode_payment_event(transaction):
        expense = Expenses.objects.create(date=str_to_datetime(transaction['postDate']),
                                          description='Pagamento de Boleto',
                                          value=transaction['amount'],
                                          scheduled=True, paid=True,
                                          bank_account='Nubank')
        expense.save()

    @staticmethod
    def _debit_withdrawalfee_event(transaction):
        location = transaction['detail'].split('-')[0].strip()

        expense = Expenses.objects.create(date=str_to_datetime(transaction['postDate']),
                                          description='Tarifa de Saque (%s)' % location,
                                          value=transaction['amount'],
                                          scheduled=True, paid=True,
                                          bank_account='Nubank')
        expense.save()

    @staticmethod
    def _debit_withdrawal_event(transaction):
        location = transaction['detail'].split('-')[0].strip()

        expense = Expenses.objects.create(date=str_to_datetime(transaction['postDate']),
                                          description='Saque (%s)' % location,
                                          value=transaction['amount'],
                                          scheduled=True, paid=True,
                                          bank_account='Nubank')
        expense.save()
