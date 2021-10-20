from validator import Validator


class Transaction:
    """
    FIELDS:
    ID, payer_name, card_number (XXXX XXXX XXXX XXXX), month, year, CVC (XXX or XXXX), payment_date, amount.

    """
    def __init__(self, ID: int, payer_name: str, card_number: int, month: int, year: int, CVC: int,
                 payment_date: str, amount: float):
        self.id = int(ID)
        self.payer_name = payer_name
        self.card_number = int(card_number)
        self.month = int(month)
        self.year = int(year)
        self.cvc = int(CVC)
        self.payment_date = payment_date
        self.amount = float(amount)

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


class TransactionCollection:
    def __init__(self):
        self.container = []

    def append(self, args):
        Validator()(self, '', *args)
        obj = Transaction(*args)
        self.container.append(obj)

    def edit_by_id(self, id, field_name, value):
        for obj in self.container:
            if obj.id == int(id) and field_name in obj.__dict__.values():
                obj_dict = obj.__dict__
                obj_dict[field_name] = value
                Validator()(self, 'edit', *[str(value) for value in obj_dict.values()])
                obj.__dict__[field_name] = value

                return obj
        return None

    def remove_object(self, obj):
        try:
            self.container.remove(obj)
        except KeyError:
            print('No such object in list')

    def remove_by_id(self, obj_id):
        try:
            for obj in self.container:
                if obj.id == obj_id:
                    self.container.remove(obj)
        except KeyError:
            pass

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
