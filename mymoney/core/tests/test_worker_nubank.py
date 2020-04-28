from datetime import datetime
from django.test import TestCase
from unittest.mock import MagicMock, Mock
from wait_for import wait_for

from pynubank import Nubank, NuException
from mymoney.core.services.nubank import NubankWorker
from mymoney.core.tests.data import card_statements
from mymoney.core.models.credit_card import CreditCardBills
from mymoney.core.models.expenses import Expenses


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

    def test_create_summary_on_expenses(self):
        self.nubank_mock.authenticate_with_qr_code = MagicMock(return_value=None)
        self.nubank_mock.get_card_statements = MagicMock(return_value=card_statements.sample1)
        self.worker.authenticate('123', '456')

        self.worker.work()

        self.assertTrue(Expenses.objects.exists())
        self.assertEqual(2, Expenses.objects.count())  # test data has items from 2 different months

    def test_payment_date(self):
        def date(day, month, only_date=False):
            d = datetime.today()
            d = d.replace(day=day, month=month)
            if only_date:
                return d.date()
            return d

        self.assertEqual(date(26, 1, only_date=True),
                         self.worker._payment_date(transaction_time=date(1, 1), closing_day=19, payment_day=26))  # <

        self.assertEqual(date(26, 2, only_date=True),
                         self.worker._payment_date(transaction_time=date(19, 1), closing_day=19, payment_day=26))  # ==

        self.assertEqual(date(26, 2, only_date=True),
                         self.worker._payment_date(transaction_time=date(20, 1), closing_day=19, payment_day=26))  # >

    def test_get_ready_status_before_start_working(self):
        ready, progress = self.worker.ready()
        self.assertFalse(ready)
        self.assertEqual(0, progress)

    def test_ready_uuid_not_found(self):
        from mymoney.core.services import nubank

        ready, progress = nubank.ready('not.found')
        self.assertFalse(ready)
        self.assertEqual(0, progress)
