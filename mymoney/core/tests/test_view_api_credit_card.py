from datetime import datetime

from django.shortcuts import resolve_url as r
from django.test import TestCase

from mymoney.core.tests import create_credit_card_bill
from mymoney.core.models.credit_card_updates import CreditCardCategoryUpdate, CreditCardDateUpdate
from mymoney.core.models.credit_card import CreditCardBills


class BurndownChartTests(TestCase):
    def test_charged_sum_zero(self):
        create_credit_card_bill({'account': '456'})
        self.response = self.client.get(r('api.credit_card.burndown_chart', datetime.now().month))
        self.assertEqual(200, self.response.status_code)

    def test_invalid_month(self):
        self.response = self.client.get(r('api.credit_card.burndown_chart', 15))
        self.assertEqual(400, self.response.status_code)


class CategoryChartTests(TestCase):
    def test_nodata_request(self):
        self.response = self.client.get(r('api.credit_card.category_chart', datetime.now().month))
        self.assertEqual(200, self.response.status_code)

    def test_single_bill(self):
        create_credit_card_bill({'category': 'casa'})

        self.response = self.client.get(r('api.credit_card.category_chart', datetime.now().month))

        self.assertEqual(self.response.content.decode(),
                         '{"labels": ["Casa"], "data": ["10"], "colors": ["#e74a3bbf"]}')

    def test_multiple_bills(self):
        create_credit_card_bill({'id': 123, 'category': 'casa', 'value': 10})
        create_credit_card_bill({'id': 456, 'category': 'estudos', 'value': 20})

        self.response = self.client.get(r('api.credit_card.category_chart', datetime.now().month))

        self.assertEqual(self.response.content.decode(),
                         '{"labels": ["Estudos", "Casa"], "data": ["20", "10"], "colors": ["#e74a3bbf", "#4e73dfbf"]}')


class UpdateCategoryTests(TestCase):
    def test_invalid_request_name_invalid(self):
        self.response = self.client.post(r('api.credit_card.update_category'))
        self.assertEqual(400, self.response.status_code)

    def test_invalid_request_no_pk(self):
        self.response = self.client.post(r('api.credit_card.update_category'), {'name': 'category', 'value': 123})
        self.assertEqual(400, self.response.status_code)

    def test_invalid_request_no_value(self):
        self.response = self.client.post(r('api.credit_card.update_category'), {'name': 'category', 'pk': 123})
        self.assertEqual(400, self.response.status_code)

    def test_item_not_found_create_one(self):
        self.response = self.client.post(r('api.credit_card.update_category'), {'name': 'category',
                                                                                'pk': 123,
                                                                                'value': 'nova categoria'})
        self.assertEqual(200, self.response.status_code)

        self.assertEqual(1, CreditCardCategoryUpdate.objects.count())

    def test_item_found_just_update(self):
        CreditCardCategoryUpdate(id=123, transaction_id=123, category='categoria antiga').save()

        self.response = self.client.post(r('api.credit_card.update_category'), {'name': 'category',
                                                                                'pk': 123,
                                                                                'value': 'nova categoria'})

        self.assertEqual(200, self.response.status_code)
        self.assertEqual(1, CreditCardCategoryUpdate.objects.count())
        self.assertEqual('nova categoria', CreditCardCategoryUpdate.objects.get(pk=123).category)


class UpdatePaymentDateTests(TestCase):
    def test_invalid_request_name_invalid(self):
        self.response = self.client.post(r('api.credit_card.update_payment_date'))
        self.assertEqual(400, self.response.status_code)

    def test_invalid_request_without_pk(self):
        self.response = self.client.post(r('api.credit_card.update_payment_date'), data={'name': 'payment_date'})
        self.assertEqual(400, self.response.status_code)

    def test_invalid_request_creditcard_bill_found_but_no_value_field(self):
        create_credit_card_bill({'id': 123})

        self.response = self.client.post(r('api.credit_card.update_payment_date'), data={'name': 'payment_date',
                                                                                         'pk': 123})
        self.assertEqual(400, self.response.status_code)

    def test_empty_database_item_not_found(self):
        self.response = self.client.post(r('api.credit_card.update_payment_date'), data={'name': 'payment_date',
                                                                                         'pk': 123})
        self.assertEqual(400, self.response.status_code)

    def test_valid_info_move_to_previous_month(self):
        create_credit_card_bill({'id': 123, 'transaction_id': 'transaction',
                                 'transaction_time': datetime.now()})

        expected_date = datetime.now().replace(month=datetime.now().month - 1).date()

        self.response = self.client.post(r('api.credit_card.update_payment_date'), data={'name': 'payment_date',
                                                                                         'pk': 123, 'value': 0})
        self.assertEqual(200, self.response.status_code)
        self.assertEqual(expected_date, CreditCardBills.objects.get(pk=123).payment_date)
        self.assertEqual(expected_date, CreditCardBills.objects.get(pk=123).closing_date)

    def test_valid_info_move_to_next_month(self):
        create_credit_card_bill({'id': 123, 'transaction_id': 'transaction',
                                 'transaction_time': datetime.now()})

        expected_date = datetime.now().replace(month=datetime.now().month + 1).date()

        self.response = self.client.post(r('api.credit_card.update_payment_date'), data={'name': 'payment_date',
                                                                                         'pk': 123, 'value': 1})
        self.assertEqual(200, self.response.status_code)
        self.assertEqual(expected_date, CreditCardBills.objects.get(pk=123).payment_date)
        self.assertEqual(expected_date, CreditCardBills.objects.get(pk=123).closing_date)

    def test_valid_info_refunded_transaction(self):
        create_credit_card_bill({'id': 123, 'transaction_id': 'transaction',
                                 'transaction_time': datetime.now()})

        self.response = self.client.post(r('api.credit_card.update_payment_date'), data={'name': 'payment_date',
                                                                                         'pk': 123, 'value': 2})
        self.assertEqual(200, self.response.status_code)
        self.assertEqual('R$0.00', str(CreditCardBills.objects.get(pk=123).value))
        self.assertFalse(CreditCardBills.objects.get(pk=123).visible)
