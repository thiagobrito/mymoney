from datetime import datetime
from django.test import TestCase
from unittest.mock import MagicMock, Mock
from wait_for import wait_for

from pynubank import Nubank, NuException
from mymoney.core.services.nubank import NubankWorker
from mymoney.core.tests.data import card_statements
from mymoney.core.models.credit_card import CreditCardBills


class NubankWorkerTest(TestCase):
    def setUp(self):
        self.nubank_mock = Nubank()
        self.nubank_mock.get_qr_code = MagicMock(return_value=('uuid_abc', None))
        self.worker = NubankWorker(nubank=self.nubank_mock)

    def test_uuid(self):
        self.worker = NubankWorker(nubank=self.nubank_mock)
        self.assertEqual('uuid_abc', self.worker.uuid)

        self.worker = NubankWorker(uuid='uuid_def')
        self.assertEqual('uuid_def', self.worker.uuid)

    def test_authenticate_failure(self):
        self.nubank_mock.authenticate_with_qr_code = Mock(side_effect=NuException(0, '', ''))
        self.assertFalse(self.worker.authenticate('123', '456'))

    def test_authenticate_already_authenticated(self):
        self.nubank_mock.authenticate_with_qr_code = MagicMock(return_value=None)
        self.nubank_mock.get_card_statements = MagicMock(return_value=[])
        self.worker.authenticate('123', '456')

        self.nubank_mock.authenticate_with_qr_code.called = False
        self.assertTrue(self.worker.authenticate('123', '456'))
        self.assertFalse(self.nubank_mock.authenticate_with_qr_code.called)

    def test_authenticate_and_processing_completed__should_load_sample_data(self):
        self.nubank_mock.authenticate_with_qr_code = MagicMock(return_value=None)
        self.nubank_mock.get_card_statements = MagicMock(return_value=card_statements.sample1)
        self.worker.authenticate('123', '456')

        wait_for(self.worker.ready)

        self.worker.work()

        self.assertTrue(CreditCardBills.objects.exists())
        self.assertEqual(54.01, float(CreditCardBills.objects.all()[0].value.amount))
        self.assertEqual(54.01, float(CreditCardBills.objects.all()[1].value.amount))
        self.assertEqual(48.12, float(CreditCardBills.objects.all()[2].value.amount))
        self.assertEqual(50, float(CreditCardBills.objects.all()[3].value.amount))

    def test_payment_date(self):
        def date(day, month, only_date=False):
            d = datetime.today()
            d = d.replace(day=day, month=month)
            if only_date:
                return d.date()
            return d

        self.assertEqual(date(19, 1, only_date=True),
                         self.worker._payment_date(transaction_time=date(1, 1), closing_day=19))  # <

        self.assertEqual(date(19, 1, only_date=True),
                         self.worker._payment_date(transaction_time=date(19, 1), closing_day=19))  # ==

        self.assertEqual(date(19, 2, only_date=True),
                         self.worker._payment_date(transaction_time=date(20, 1), closing_day=19))  # >
