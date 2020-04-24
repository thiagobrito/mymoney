import datetime
from pynubank import Nubank, NuException

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

        self._authenticated = False

    def authenticate(self, login, password):
        if self._authenticated:
            return True

        try:
            self._nu.authenticate_with_qr_code(login, password, self.uuid)
            self._authenticated = True
            PROCESS_QUEUE.add(self.uuid, self)

        except NuException:
            pass

        return self._authenticated

    def work(self):
        if self._authenticated:
            for statement in self._nu.get_card_statements():
                if CreditCardBills.objects.filter(account=statement['account'],
                                                  transaction_id=statement['id']).exists():
                    continue

                obj = CreditCardBills(account=statement['account'], transaction_id=statement['id'],
                                      description=statement['description'], value=statement['amount'],
                                      time=statement['time'], category=statement['title'],
                                      payment_date=datetime.datetime.today())
                obj.save()

            self._ready = True

        return False

    def ready(self):
        return self._ready


def authenticate(uuid, login, password):
    worker = NubankWorker(uuid)
    return worker.authenticate(login, password)


def ready(uuid):
    worker = PROCESS_QUEUE.locate(uuid)
    if worker:
        return worker.ready()
