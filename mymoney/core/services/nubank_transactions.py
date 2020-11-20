import uuid
import os
import json
import datetime
from pynubank import Nubank

from mymoney.core.util import str_to_datetime


class NubankTransactions:
    def __init__(self, nubank=None):
        self.__nubank = nubank
        self.uuid = str(uuid.uuid4())

    def authenticate(self, cpf, password, uuid):
        self._nubank().authenticate_with_qr_code(cpf, password, uuid)

    def transactions(self, min_year=2020):
        for bill in self._get_bills():
            if self._should_get_bill_details(bill, min_year):
                bill_details = self._get_bill_details(bill)
                for transaction in bill_details['bill']['line_items']:
                    yield {
                        'bill': self._prepare_date_fields(bill['summary']),
                        'transaction': self._prepare_date_fields(transaction)
                    }

    def _nubank(self):
        if self.__nubank is None:
            self.__nubank = Nubank()
        return self.__nubank

    def _get_bills(self):
        bills_path = r'data\bills.json'
        if os.path.exists(bills_path):
            return json.loads(open(bills_path, 'r').read())
        bills = self._nubank().get_bills()
        if os.path.exists(r'data'):
            open(bills_path, 'w').write(json.dumps(bills))
        return bills

    def _prepare_date_fields(self, info):
        date_fields = ['due_date', 'close_date', 'post_date', 'open_date']
        for field in date_fields:
            if field in info:
                info[field] = str_to_datetime(info[field])
        return info

    @staticmethod
    def _should_get_bill_details(bill, min_year):
        if bill['state'] == 'open' or bill['state'] == 'overdue':
            bill_close_date = datetime.datetime.strptime(bill['summary']['close_date'], "%Y-%m-%d")
            return bill_close_date.year >= min_year

    def _get_bill_details(self, bill):
        details_path = r'data\bill_details_%s.json' % bill['summary']['due_date']
        if os.path.exists(details_path):
            return json.loads(open(details_path, 'r').read())
        bill_details = self._nubank().get_bill_details(bill)
        if os.path.exists(r'data'):
            open(details_path, 'w').write(json.dumps(bill_details, indent=2))
        return bill_details
