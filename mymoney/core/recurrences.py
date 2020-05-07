from mymoney.core.models.expenses import Expenses


def has_pending_recurrences(month):
    year = 2020
    previous_month_expenses = Expenses.objects.filter(date__year=year, date__month=month - 1, credit_card_ref='',
                                                      recurrent=True)
    current_month_expenses = Expenses.objects.filter(date__year=year, date__month=month)

    for prev_expense in previous_month_expenses:
        prev_description, should_create = _check_description(prev_expense.description)

        found = False
        for curr_expense in current_month_expenses:
            curr_description, _ = _check_description(curr_expense.description)

            if curr_description == prev_description:
                found = True
                break

        if not found and should_create:
            return True

    return False


def fill_pending_recurrences(month):
    year = 2020
    previous_month_expenses = Expenses.objects.filter(date__year=year, date__month=month - 1, credit_card_ref='',
                                                      recurrent=True)
    current_month_expenses = Expenses.objects.filter(date__year=year, date__month=month)

    for prev_expense in previous_month_expenses:
        prev_description, should_create = _check_description(prev_expense.description)

        found = False
        for curr_expense in current_month_expenses:
            curr_description, _ = _check_description(curr_expense.description)

            if curr_description == prev_description:
                curr_expense.recurrent = True
                curr_expense.save()

                found = True
                break

        if not found and should_create:
            Expenses(date=prev_expense.date.replace(month=prev_expense.date.month + 1),
                     description=prev_expense.description, value=prev_expense.value, recurrent=True).save()


def _check_description(description):
    should_create = True
    if '(' in description and '/' in description:
        pos = description.find('(')
        description = description[:pos].strip()
        should_create = False

    return description, should_create
