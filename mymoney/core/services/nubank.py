import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

from pynubank import Nubank

from mymoney.core import util
from mymoney.core.models.credit_card import CreditCardBills
from mymoney.core.models.credit_card_updates import CreditCardCategoryUpdate
from mymoney.core.models.expenses import Expenses
from mymoney.core.services.processing import WorkerBase
from mymoney.core.services.nubank_transactions import NubankCardTransactions
from mymoney.core.services.nuconta_transactions import NuContaTransactions

from mymoney.settings import PROCESS_QUEUE


class NubankWorker(WorkerBase):
    def __init__(self, account, card_transactions=None, conta_transactions=None):
        super(NubankWorker, self).__init__()

        self._card_transactions = card_transactions or NubankCardTransactions()
        self._conta_transactions = conta_transactions or NuContaTransactions()
        self.uuid = self._card_transactions.uuid
        self._account = account
        self._status = {'ready': False, 'progress': 0, 'exception': False}

    def work(self):
        CreditCardBills.objects.filter(account=self._account).delete()

        self._save_all_transactions()
        self._save_expenses_table_bill_record()

        self._status['ready'] = True

    def status(self):
        return self._status

    def _save_all_transactions(self):
        for transaction in self._card_transactions.transactions():
            self._save_single_transaction(transaction['bill'], transaction['transaction'])

        self._conta_transactions.load_all_transactions()

    def _save_single_transaction(self, bill, transaction):
        if self._is_buy_transaction(transaction):
            charge_index = transaction['index'] + 1
            charge_count = transaction['charges']

            description = transaction['title']
            if transaction['charges'] > 1:
                description += ' (%d/%d)' % (charge_index, charge_count)

            obj = CreditCardBills(account=self._account,
                                  transaction_id=transaction['id'],
                                  description=description,
                                  value=util.format_money(transaction['amount']),
                                  transaction_time=transaction['post_date'],
                                  category=self._transaction_category(transaction),
                                  payment_date=bill['due_date'], closing_date=bill['close_date'],
                                  charge_index=charge_index, charge_count=charge_count)
            obj.save()

    @staticmethod
    def _is_buy_transaction(transaction):
        return 'charges' in transaction

    @staticmethod
    def _transaction_category(transaction):
        try:
            return CreditCardCategoryUpdate.objects.get(transaction_id=transaction['id']).category
        except ObjectDoesNotExist:
            return transaction['category']

    @staticmethod
    def _save_expenses_table_bill_record():
        bills = CreditCardBills.objects.filter(payment_date__year=datetime.datetime.now().year) \
            .values('payment_date') \
            .annotate(total=Sum('value')) \
            .values('account', 'payment_date', 'total') \
            .order_by('payment_date')

        for bill in bills:
            try:
                obj = Expenses.objects.get(credit_card_ref=bill['account'], date=bill['payment_date'])
                obj.value = bill['total']
                obj.save()

            except ObjectDoesNotExist:
                obj = Expenses(date=bill['payment_date'],
                               description='Credit Card (%s)' % bill['account'],
                               value=bill['total'],
                               credit_card_ref=bill['account'],
                               bank_account='BRD')
                obj.save()


def authenticate(login, password, uuid):
    nubank = Nubank()
    nubank.authenticate_with_qr_code(login, password, uuid)

    nucard_transactions = NubankCardTransactions(nubank=nubank)
    nuconta_transactions = NuContaTransactions(nubank=nubank)

    return NubankWorker(login, card_transactions=nucard_transactions, conta_transactions=nuconta_transactions)


def add_to_queue(uuid, worker):
    PROCESS_QUEUE.add(uuid, worker)


def status(uuid):
    worker = PROCESS_QUEUE.locate(uuid)
    if worker:
        return worker.status()
    return {'ready': False, 'progress': 0, 'exception': False}
