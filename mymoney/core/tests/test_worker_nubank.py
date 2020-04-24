from django.test import TestCase
from unittest.mock import MagicMock, Mock
from wait_for import wait_for

from pynubank import Nubank, NuException
from mymoney.core.services.nubank import NubankWorker
from mymoney.core.tests.data import card_statements


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
