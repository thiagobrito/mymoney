from datetime import datetime
from pynubank import Nubank
from mymoney.core.services.nubank import NubankWorker

from mymoney.core.tests.data.full_card_statements import sample_full
from unittest.mock import MagicMock


def fill_database():
    nubank_mock = Nubank()
    nubank_mock.get_qr_code = MagicMock(return_value=('uuid_abc', None))
    worker = NubankWorker(nubank=nubank_mock)

    nubank_mock.authenticate_with_qr_code = MagicMock(return_value=None)
    nubank_mock.get_card_statements = MagicMock(return_value=sample_full)
    worker.authenticate('123', '456')

    worker.work()


def date(day, month, only_date=False):
    d = datetime.today()
    d = d.replace(day=day, month=month)
    if only_date:
        return d.date()
    return d
