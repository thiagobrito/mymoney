from datetime import datetime
from mymoney.core.models.expenses import Expenses

from mymoney.core.util import add_months


def has_pending_recurrences(month, year):
    previous_month = add_months(datetime(year=year, month=month, day=1), -1)

    previous_month_expenses = Expenses.objects.filter(date__year=previous_month.year, date__month=previous_month.month,
                                                      transaction_id='', recurrent=True)
    current_month_expenses = Expenses.objects.filter(date__year=year, date__month=month)

    for prev_expense in previous_month_expenses:
        prev_description, has_future_payment = _check_description(prev_expense.description)
        if has_future_payment:
            found = False
            for curr_expense in current_month_expenses:
                curr_description, _ = _check_description(curr_expense.description)

                if curr_description == prev_description:
                    found = True
                    break

            if not found:
                return True

    return False


def fill_pending_recurrences(month, year):
    previous_month = add_months(datetime(year=year, month=month, day=1), -1)
    previous_month_expenses = Expenses.objects.filter(date__year=previous_month.year, date__month=previous_month.month,
                                                      transaction_id='', recurrent=True)

    current_month_expenses = Expenses.objects.filter(date__year=year, date__month=month)

    for prev_expense in previous_month_expenses:
        prev_description, has_future_payment = _check_description(prev_expense.description)
        if has_future_payment:
            found = False
            for curr_expense in current_month_expenses:
                curr_description, _ = _check_description(curr_expense.description)

                if curr_description == prev_description:
                    curr_expense.recurrent = True
                    curr_expense.save()

                    found = True
                    break

            if not found:
                Expenses(date=add_months(prev_expense.date, 1),
                         description=_update_portion_payment(prev_expense.description), value=prev_expense.value,
                         recurrent=True).save()


def _check_description(description):
    clean_description = description

    has_future_payment = True
    if '(' in description and '/' in description:
        pos = description.find('(')
        clean_description = description[:pos].strip()

        payments = description[pos:].replace('(', '').replace(')', '').split('/')
        if payments[0] == payments[1]:
            has_future_payment = False

    return clean_description, has_future_payment


def _update_portion_payment(description):
    if '(' in description and '/' in description:
        pos = description.find('(')
        cleaned_description = description[:pos].strip()

        payments = description[pos:].replace('(', '').replace(')', '').split('/')
        return '%s (%d/%d)' % (cleaned_description, int(payments[0]) + 1, int(payments[1]))

    return description
