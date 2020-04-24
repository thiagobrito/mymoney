import calendar
import datetime
from pynubank import Nubank, NuException
from django.db import transaction

from mymoney.settings import PROCESS_QUEUE
from mymoney.core.services.processing import WorkerBase
from mymoney.core.models.credit_card import CreditCardBills


class NubankWorker(WorkerBase):
    def __init__(self, uuid=None, nubank=None):
        super(NubankWorker, self).__init__()

        self._nu = nubank or Nubank()
        if uuid:
            self.uuid = uuid
        else:
            self.uuid, _ = self._nu.get_qr_code()

        self._login = None
        self._authenticated = False

    def authenticate(self, login, password):
        if self._authenticated:
            return True

        try:
            self._nu.authenticate_with_qr_code(login, password, self.uuid)
            self._authenticated = True
            self._login = login

            PROCESS_QUEUE.add(self.uuid, self)

        except NuException:
            pass

        return self._authenticated

    @transaction.atomic
    def work(self):
        if self._authenticated:
            for statement in self._nu.get_card_statements():
                payment_date = self._payment_date(statement['time'], 19)
                if payment_date.year > 2018:
                    if CreditCardBills.objects.filter(account=self._login, transaction_id=statement['id']).exists():
                        continue

                    obj = CreditCardBills(account=self._login, transaction_id=statement['id'],
                                          description=statement['description'], value=statement['amount'],
                                          transaction_time=statement['time'], category=statement['title'],
                                          payment_date=payment_date)
                    obj.save()

            self._ready = True

        return False

    def ready(self):
        return self._ready

    def _payment_date(self, transaction_time, closing_day):
        def add_months(sourcedate, months):
            month = sourcedate.month - 1 + months
            year = sourcedate.year + month // 12
            month = month % 12 + 1
            day = min(sourcedate.day, calendar.monthrange(year, month)[1])
            return datetime.date(year, month, day)

        if type(transaction_time) == str:
            transaction_time = datetime.datetime.strptime(transaction_time, "%Y-%m-%dT%H:%M:%SZ")

        d = datetime.date.today()
        d = d.replace(year=transaction_time.year, month=transaction_time.month, day=transaction_time.day)

        if d.day > closing_day:
            d = add_months(d, 1)

        return d.replace(day=closing_day)


def authenticate(uuid, login, password):
    worker = NubankWorker(uuid)
    return worker.authenticate(login, password)


def ready(uuid):
    worker = PROCESS_QUEUE.locate(uuid)
    if worker:
        return worker.ready()
