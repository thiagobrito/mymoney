import os
import json
import datetime
from pynubank import Nubank


class NubankTransactions:
    def __init__(self, nubank=None):
        self._nubank = nubank or Nubank()
        self.uuid, _ = self._nubank.get_qr_code()

    def authenticate(self, cpf, password, uuid):
        self._nubank.authenticate_with_qr_code(cpf, password, uuid)

    def transactions(self, min_year=2020):
        for bill in self._get_bills():
            if self._should_get_bill_details(bill, min_year):
                bill_details = self._get_bill_details(bill)
                for transaction in bill_details['bill']['line_items']:
                    yield {
                        'bill': bill['summary'],
                        'transaction': transaction
                    }

    def _get_bills(self):
        bills_path = r'data\bills.json'
        if os.path.exists(bills_path):
            return json.loads(open(bills_path, 'r').read())
        bills = self._nubank.get_bills()
        open(bills_path, 'r').write(json.dumps(bills))
        return bills

    @staticmethod
    def _should_get_bill_details(bill, min_year):
        if bill['state'] == 'open' or bill['state'] == 'overdue':
            bill_close_date = datetime.datetime.strptime(bill['summary']['close_date'], "%Y-%m-%d")
            return bill_close_date.year >= min_year

    def _get_bill_details(self, bill):
        details_path = r'data\bill_details_%s.json' % bill['summary']['due_date']
        if os.path.exists(details_path):
            return json.loads(open(details_path, 'r').read())
        bill_details = self._nubank.get_bill_details(bill)
        open(details_path, 'w').write(json.dumps(bill_details, indent=2))
        return bill_details
