from django.shortcuts import resolve_url as r
from django.test import TestCase
from unittest import mock


class IndexTest(TestCase):
    def test_nubank_summary_page(self):
        self.response = self.client.get(r('nubank.summary'))
        self.assertEqual(200, self.response.status_code)


class NubankProcessingTest(TestCase):
    def test_login_view(self):
        self.assertEqual(200, self.client.get(r('nubank.login')).status_code)

    def test_qrcode_view(self):
        self.assertEqual(200, self.client.post(r('nubank.qrcode'),
                                               data={'login': 'user123', 'password': 'password'}).status_code)

        self.assertIsNotNone(self.client.session.get('uuid'))
        self.assertEqual('user123', self.client.session.get('login'))
        self.assertEqual('password', self.client.session.get('password'))

    def test_qrcode_view_without_login_should_redirect(self):
        self.assertEqual(302, self.client.post(r('nubank.qrcode'),
                                               data={'login': 'user123'}).status_code)

    def test_qrcode_view_without_password_should_redirect(self):
        self.assertEqual(302, self.client.post(r('nubank.qrcode'),
                                               data={'password': 'password'}).status_code)

    def test_authenticate_and_process_without_login_should_return_401(self):
        self.assertEqual(401, self.client.get(r('nubank.authenticate')).status_code)

    @mock.patch('mymoney.core.services.nubank.authenticate', return_value=True)
    @mock.patch('mymoney.core.services.nubank.add_to_queue', return_value=True)
    def test_authenticate_and_process_with_login_information_return_processing_message(self, authenticate, add_queue):
        session = self.client.session
        session['uuid'] = 'uuid'
        session['login'] = 'user123'
        session['password'] = 'pass'
        session.save()

        self.assertEqual(200, self.client.get(r('nubank.authenticate')).status_code)

        self.assertIsNone(self.client.session.get('password'))

    def test_processing_uuid_undefined_return_401(self):
        self.assertEqual(401, self.client.get(r('nubank.processing')).status_code)

    @mock.patch('mymoney.core.services.nubank.status', return_value={'ready': False, 'progress': 0, 'exception': False})
    def test_processing_uuid_defined_return_status(self, status):
        session = self.client.session
        session['uuid'] = 'uuid'
        session.save()

        self.assertEqual(200, self.client.get(r('nubank.processing')).status_code)

    def test_summary(self):
        self.assertEqual(200, self.client.post(r('nubank.summary')).status_code)
