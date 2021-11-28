from validator import Validator, ValidatorWrapper


class Transaction:
    """
    FIELDS:
    ID, payer_name, card_number (XXXX XXXX XXXX XXXX), month, year, CVC (XXX or XXXX), payment_date, amount.

    """
    def __init__(self, ID: int, payer_name: str, card_number: int, month: int, year: int, CVC: int,
                 payment_date: str, amount: float):
        self.id = int(ID)
        self.set_payer_name(payer_name)
        self.set_card_number(card_number)
        self.set_month(month)
        self.set_year(year)
        self.set_payment_date(payment_date)
        self.set_cvc(CVC)
        self.set_amount(amount)

    @ValidatorWrapper.validate_amount
    def set_amount(self, amount):
        self.amount = float(amount)

    @ValidatorWrapper.validate_cvc
    def set_cvc(self, cvc):
        self.cvc = int(cvc)

    @ValidatorWrapper.validate_payer_name
    def set_payer_name(self, payer_name):
        self.payer_name = payer_name

    @ValidatorWrapper.validate_card_number
    def set_card_number(self, card_number):
        self.card_number = int(card_number)

    @ValidatorWrapper.validate_month
    def set_month(self, month):
        self.month = int(month)

    @ValidatorWrapper.validate_year
    def set_year(self, year):
        self.year = int(year)

    @ValidatorWrapper.validate_payment_date
    def set_payment_date(self, payment_date):
        self.payment_date = payment_date

    def to_dict(self):
        return self.__dict__

    def __getitem__(self, item):
        return self.__dict__[item]

    def __lt__(self, other):
        boolean_list = []
        for key in self.__dict__:
            try:
                boolean_list.append(self.__dict__[key] < other.__dict__[key])
            except TypeError:
                continue
        return boolean_list.count(True) > boolean_list.count(False)

    def __str__(self):
        return ',\n'.join(f'{key}: {value}'.replace('_', ' ') for key, value in self.__dict__.items()) + ','

    def __setattr__(self, key, value):
        self.__dict__[key] = value


class TransactionCollection:
    def __init__(self):
        self.container = []

    def append(self, args):
        obj = Transaction(*args)
        self.container.append(obj)

    @Validator.validate_concrete_value
    def edit_by_id(self, id, field_name, value):
        for obj in self.container:
            if obj.id == int(id) and field_name in obj.__dict__.keys():
                obj_dict = obj.__dict__
                obj_dict[field_name] = value
                # Validator()(self, *[str(value) for value in obj_dict.values()])
                setattr(obj, field_name, value)

                return obj
        return None

    def remove_object(self, obj):
        try:
            self.container.remove(obj)
        except ValueError:
            print('No such object in list')

    def remove_by_id(self, obj_id):
        for obj in self.container:
            if obj.id == obj_id:
                self.container.remove(obj)

    def get_values(self, field_name):
        return [obj.__dict__[field_name] for obj in self.container]

    def get_data_in_dicts(self):
        return [obj.to_dict() for obj in self.container]

    def find_by_id(self, obj_id):
        for obj in self.container:
            if obj.id == obj_id:
                return obj

    def sort(self):
        return sorted(self.container)

    def __str__(self):
        return '\n------------------------------------------------------\n'.join(str(trans) for trans in self.container)
