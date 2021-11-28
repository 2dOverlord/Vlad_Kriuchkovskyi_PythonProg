from datetime import date


class ValidatorException(BaseException):
    def __init__(self, obj_id, field_name, message=''):
        self.obj_id = obj_id
        self.field_name = field_name
        self.message = message

    def get_field_name(self):
        return self.field_name

    def __str__(self):
        return self.message


class ValidatorWrapper:
    @staticmethod
    def initializer(obj):
        validator = Validator()
        validator.obj_id = obj.id
        return validator

    @staticmethod
    def validate_payer_name(func):
        def wrapper(obj, payer_name):
            validator = ValidatorWrapper.initializer(obj)
            validator.check_payer_name(payer_name)
            func(obj, payer_name)
        return wrapper

    @staticmethod
    def validate_card_number(func):
        def wrapper(obj, card_number):
            validator = ValidatorWrapper.initializer(obj)
            validator.check_if_possible_to_int(card_number=card_number)
            validator.check_card_number(card_number)
            func(obj, card_number)
        return wrapper

    @staticmethod
    def validate_month(func):
        def wrapper(obj, month, *args):
            validator = ValidatorWrapper.initializer(obj)
            validator.check_if_possible_to_int(month=month)
            validator.check_month(month)
            func(obj, month)
        return wrapper

    @staticmethod
    def validate_year(func):
        def wrapper(obj, year, *args):
            validator = ValidatorWrapper.initializer(obj)
            validator.check_if_possible_to_int(year=year)
            validator.check_year(year)
            func(obj, year)
        return wrapper

    @staticmethod
    def validate_payment_date(func):
        def wrapper(obj, date):
            validator = ValidatorWrapper.initializer(obj)
            validator.check_payment_date(date)
            func(obj, date)
        return wrapper

    @staticmethod
    def validate_cvc(func):
        def wrapper(obj, cvc):
            validator = ValidatorWrapper.initializer(obj)
            validator.check_if_possible_to_int(cvc=cvc)
            validator.check_cvc(cvc)
            func(obj, cvc)
        return wrapper

    @staticmethod
    def validate_amount(func):
        def wrapper(obj, amount):
            validator = ValidatorWrapper.initializer(obj)
            validator.check_amount(amount)
            func(obj, amount)
        return wrapper


class Validator:
    def __init__(self):
        pass

    def __call__(self, ID: int, payer_name: str, card_number: int, month: int, year: int, CVC: int,
                 payment_date: str, amount: float, *args, **kwargs):
        self.obj_id = ID
        self.check_if_possible_to_int(id=ID, card_number=card_number, month=month, year=year, cvc=CVC)
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

    @staticmethod
    def validate(func):
        def wrapped(*args, **kwargs):
            validator = Validator()
            validator(*args)
            value = func(*args, **kwargs)
            return value
        return wrapped

    @staticmethod
    def validate_concrete_value(func):
        def wrapped(*args, **kwargs):
            obj_id = args[1]
            field_name, value = kwargs.values()
            print(field_name, value)
            validator = Validator()
            validator.obj_id = obj_id
            val_dict = {
                'payer_name': validator.check_payer_name,
                'card_number': validator.check_card_number,
                'month': validator.check_month,
                'year': validator.check_year,
                'cvc': validator.check_cvc,
                'payment_date': validator.check_payment_date,
                'amount': validator.check_amount,
            }
            val_dict[field_name](value)
            args = list(args) + list(kwargs.values())
            return func(*args)
        return wrapped