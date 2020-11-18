from django.test import TestCase
from unittest.mock import MagicMock, Mock

from pynubank import Nubank, NuException, MockHttpClient
from mymoney.core.services.nubank import NubankWorker
from mymoney.core.tests.data import card_statements
from mymoney.core.models.credit_card import CreditCardBills
from mymoney.core.models.credit_card_updates import CreditCardCategoryUpdate, CreditCardDateUpdate
from mymoney.core.models.expenses import Expenses
from mymoney.core.tests import util

'''
class NubankWorkerTest(TestCase):
    def setUp(self):
        self.nubank = Nubank(MockHttpClient())
        self.worker = NubankWorker(nubank=self.nubank)
        self.worker.authenticate('123', '456')

    def test_uuid(self):
        self.worker = NubankWorker(uuid='uuid_def')
        self.assertEqual('uuid_def', self.worker.uuid)

    def test_authenticate_and_processing_completed__should_load_sample_data(self):
        self.nubank.get_card_statements = MagicMock(return_value=card_statements.sample1)
        self.worker.work()

        self.assertTrue(CreditCardBills.objects.exists())
        self.assertEqual(54.01, float(CreditCardBills.objects.all()[0].value.amount))
        self.assertEqual(54.01, float(CreditCardBills.objects.all()[1].value.amount))
        self.assertEqual(48.12, float(CreditCardBills.objects.all()[2].value.amount))
        self.assertEqual(50, float(CreditCardBills.objects.all()[3].value.amount))

    def test_create_summary_on_expenses(self):
        self.nubank.get_card_statements = MagicMock(return_value=card_statements.sample1)

        self.worker.work()

        self.assertTrue(Expenses.objects.exists())
        self.assertEqual(2, Expenses.objects.count())  # test data has items from 2 different months

    def test_payment_date_new_item(self):
        statement = {'time': util.date(1, 1), 'id': 'not.found'}
        self.assertEqual(util.date(26, 1, only_date=True),
                         self.worker._calculate_payment_date(statement, closing_day=19, payment_day=26))  # <

        statement['time'] = util.date(19, 1)
        self.assertEqual(util.date(26, 2, only_date=True),
                         self.worker._calculate_payment_date(statement, closing_day=19, payment_day=26))  # ==

        statement['time'] = util.date(20, 1)
        self.assertEqual(util.date(26, 2, only_date=True),
                         self.worker._calculate_payment_date(statement, closing_day=19, payment_day=26))  # >

    def test_payment_date_updated_item(self):
        transaction_time = util.date(1, 1)
        new_payment_date = util.date(26, 4, only_date=True)
        statement = {'time': transaction_time, 'id': '{valid_transaction}'}

        obj = CreditCardDateUpdate(transaction_id=statement['id'],
                                   orig_transaction_time=transaction_time,
                                   orig_payment_date=util.date(26, 1, only_date=True),
                                   new_payment_date=new_payment_date,
                                   new_closing_date=util.date(19, 4, only_date=True))
        obj.save()

        self.assertEqual(new_payment_date,
                         self.worker._calculate_payment_date(statement, closing_day=19, payment_day=26))  # <

    def test_get_ready_status_before_start_working(self):
        status = self.worker.status()
        self.assertFalse(status['ready'])
        self.assertEqual(0, status['progress'])

    def test_ready_uuid_not_found(self):
        from mymoney.core.services import nubank

        status = nubank.status('not.found')
        self.assertFalse(status['ready'])
        self.assertEqual(0, status['progress'])

    def test_category_updated_should_update_transaction_category(self):
        obj = CreditCardCategoryUpdate(transaction_id=card_statements.sample1[0]['id'],
                                       category='testing category')
        obj.save()

        self.nubank.get_card_statements = MagicMock(return_value=card_statements.sample1)
        self.worker.work()

        obj = CreditCardBills.objects.get(transaction_id=card_statements.sample1[0]['id'])
        self.assertEqual('testing category', obj.category)
'''