import datetime
from pynubank import Nubank, NuException

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Sum

from mymoney.settings import PROCESS_QUEUE
from mymoney.core.services.processing import WorkerBase
from mymoney.core.models.credit_card import CreditCardBills
from mymoney.core.models.credit_card_updates import CreditCardCategoryUpdate, CreditCardDateUpdate
from mymoney.core.models.expenses import Expenses

from mymoney.core import util

DEFAULT_PAYMENT_DAY = 26
DEFAULT_CLOSING_DAY = 19


class NubankWorker(WorkerBase):
    def __init__(self, uuid=None, nubank=None):
        super(NubankWorker, self).__init__()

        self._nu = nubank or Nubank()
        if uuid:
            self.uuid = uuid
        else:
            self.uuid, _ = self._nu.get_qr_code()

        self._progress = 0
        self._login = None
        self._status = {'authenticated': False, 'progress': 0, 'ready': False, 'failed': False}
        self._card_statements = None

    def authenticate(self, login, password):
        if self._status['authenticated']:
            return True

        try:
            self._nu.authenticate_with_qr_code(login, password, self.uuid)
            self._login = login
            self._card_statements = self._nu.get_card_statements()

            PROCESS_QUEUE.add(self.uuid, self)
            self._status['authenticated'] = True

        except NuException:
            self._status['failed'] = True

        return self._status['authenticated']

    @transaction.atomic
    def work(self):
        if self._status['authenticated']:
            # !!!! WARNING: Remove this item when finish this step !!!!!!!!
            CreditCardBills.objects.filter(account=self._login).delete()

            self._save_bills()
            self._save_expense_table_record()

            self._status['ready'] = True

    def status(self):
        return self._status

    def _save_bills(self):
        total = len(self._card_statements)

        account_credit_card_bills = CreditCardBills.objects.filter(account=self._login)

        for index, statement in enumerate(self._card_statements):
            payment_date = self._calculate_payment_date(statement, DEFAULT_CLOSING_DAY, DEFAULT_PAYMENT_DAY)
            if payment_date.year > 2018:
                if account_credit_card_bills.filter(transaction_id=statement['id']).exists():
                    continue

                self._status['progress'] = (index / total) * 100.0

                if 'details' in statement and 'charges' in statement['details']:
                    charge_count = statement['details']['charges']['count']
                    charge_amount = util.format_money(statement['details']['charges']['amount'])

                    visible = True
                    for desc in ['Casas Bahia.C*219987898']:
                        if desc in statement['description']:
                            visible = False
                            break

                    for charge_index in range(1, charge_count + 1):
                        charge_payment_date = util.add_months(payment_date, charge_index - 1)

                        description = '%s (%d/%d)' % (statement['description'], charge_index, charge_count)

                        obj = CreditCardBills(account=self._login,
                                              transaction_id=statement['id'],
                                              description=description,
                                              value=charge_amount,
                                              transaction_time=statement['time'],
                                              category=self._transaction_category(statement),
                                              payment_date=charge_payment_date,
                                              closing_date=charge_payment_date.replace(day=DEFAULT_CLOSING_DAY),
                                              charge_count=charge_count,
                                              visible=visible)
                        obj.save()

                else:
                    obj = CreditCardBills(account=self._login,
                                          transaction_id=statement['id'],
                                          description=statement['description'],
                                          value=util.format_money(statement['amount']),
                                          transaction_time=statement['time'],
                                          category=self._transaction_category(statement),
                                          payment_date=payment_date,
                                          closing_date=payment_date.replace(day=DEFAULT_CLOSING_DAY),
                                          charge_count=1)
                    obj.save()

    def _save_expense_table_record(self):
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

    def _calculate_payment_date(self, statement, closing_day, payment_day):
        transaction_time = statement['time']
        if type(transaction_time) == str:
            transaction_time = datetime.datetime.strptime(transaction_time, "%Y-%m-%dT%H:%M:%SZ")

        d = datetime.date.today()
        d = d.replace(year=transaction_time.year, month=transaction_time.month, day=transaction_time.day)

        if d.day >= closing_day:
            d = util.add_months(d, 1)

        calculated_date = d.replace(day=payment_day)

        try:
            updated_obj = CreditCardDateUpdate.objects.get(transaction_id=statement['id'],
                                                           orig_transaction_time=transaction_time,
                                                           orig_payment_date=calculated_date)
            return updated_obj.new_payment_date

        except ObjectDoesNotExist:
            pass

        return calculated_date

    def _transaction_category(self, statement):
        try:
            return CreditCardCategoryUpdate.objects.get(transaction_id=statement['id']).category
        except ObjectDoesNotExist:
            return statement['title']


def authenticate(uuid, login, password):
    worker = NubankWorker(uuid)
    return worker.authenticate(login, password)


def status(uuid):
    worker = PROCESS_QUEUE.locate(uuid)
    if worker:
        return worker.status()
    return {'ready': False, 'progress': 0, 'exception': False}
