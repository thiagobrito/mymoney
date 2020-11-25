from datetime import datetime
from mymoney.core.models.credit_card import CreditCardBills


def create_credit_card_bill(kwargs):
    data = {'id': 123, 'account': '123', 'transaction_id': '456', 'description': 'bill(1)',
            'value': 10, 'transaction_time': datetime.now(), 'payment_date': datetime.now(),
            'closing_date': datetime.now(), 'category': 'teste', 'charge_count': 1, 'charge_index': 1,
            'visible': True}
    data.update(kwargs)

    obj = CreditCardBills(id=data['id'], account=data['account'], transaction_id=data['transaction_id'],
                          description=data['description'], value=data['value'],
                          transaction_time=data['transaction_time'], payment_date=data['payment_date'],
                          closing_date=data['closing_date'], category=data['category'],
                          charge_count=data['charge_count'], charge_index=data['charge_index'],
                          visible=data['visible'])
    obj.save()
