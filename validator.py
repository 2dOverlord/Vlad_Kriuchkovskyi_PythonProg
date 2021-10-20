from datetime import date


class ValidatorException(BaseException):
    def __init__(self, obj_id, field_name, message=''):
        self.field_name = field_name
        self.message = message

    def get_field_name(self):
        return self.field_name

    def __str__(self):
        return self.message


class Validator:
    def __init__(self):
        pass

    def __call__(self, collector, mode, ID: int, payer_name: str, card_number: int, month: int, year: int, CVC: int,
                 payment_date: str, amount: float, *args, **kwargs):
        self.collector = collector

        self.obj_id = ID
        self.check_if_possible_to_int(id=ID, card_number=card_number, month=month, year=year, cvc=CVC)
        # if not mode == 'edit':
        #     self.check_if_unique('id', ID)
        self.check_payer_name(payer_name)
        self.check_card_number(card_number)
        self.check_month(month)
        self.check_year(year)
        self.check_cvc(CVC)
        self.check_payment_date(payment_date)
        self.check_amount(amount)

    def check_if_possible_to_int(self, **kwargs):
        for field_name, value in kwargs.items():
            try:
                int(value)
            except ValueError:
                raise ValidatorException(self.obj_id, field_name, f'{field_name} must be an integer value')

    def check_if_unique(self, field_name, value):
        values = self.collector.get_values(field_name)
        if value in values:
            raise ValidatorException(self.obj_id, field_name, f'{field_name} must be UNIQUE parameter')

    def check_payer_name(self, payer_name):
        if not payer_name.isalpha():
            raise ValidatorException(self.obj_id, 'payer_name', 'Payer name must not contain anything except of letters')


    def check_card_number(self, card_number):
        if not len(card_number) == 16:
            raise ValidatorException(self.obj_id, 'card_number', 'Card number must contain 16 numbers')

    def check_month(self, month):
        if int(month) > 12 or int(month) < 1:
            raise ValidatorException(self.obj_id, 'month', 'There is no such month')

    def check_year(self, year):
        if int(year) < int(date.today().year):
            raise ValidatorException(self.obj_id, 'year', 'Year on your card must be more or equal to an actual year')
        if int(year) - int(date.today().year) > 10:
            raise ValidatorException(self.obj_id, 'year', 'Well, maybe you know bank where you can create a card for 10 years ahead,'
                                             ' but Im not, so **** you')

    def check_cvc(self, cvc):
        if not len(cvc) == 3 and not len(cvc) == 4:
            raise ValidatorException(self.obj_id, 'cvc', 'Your cvc is not in the right format')

    def check_payment_date(self, payment_date):
        day = int(payment_date[0:2])
        month = int(payment_date[3:5])
        year = int(payment_date[6:])
        today = date.today()
        if year > today.year or year < 1990:
            raise ValidatorException(self.obj_id, 'payment_date', 'There is a problem in payment date`s year')
        if (month > today.month and year == today.year) or month > 12 or month < 1:
            raise ValidatorException(self.obj_id, 'payment_date', 'There is a problem in payment date`s month')
        if (day > today.day and month == today.month and year == today.year) or day > 31 or day < 1:
            raise ValidatorException(self.obj_id, 'payment_date', 'There is a problem in payment date`s day')

    def check_amount(self, amount):
        try:
            amount = float(amount)
            if amount < 1:
                raise ValidatorException(self.obj_id, 'amount', 'Your amount is lower than 1')
        except TypeError:
            raise ValidatorException(self.obj_id, 'amount', 'Amount must be Float or Int number')