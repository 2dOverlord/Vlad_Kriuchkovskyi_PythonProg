from abc import abstractmethod
from custom_exceptions import ValidationError


class BaseTask:
    def __init__(self, task_name: str, task_description: str):
        self.task_name = task_name
        self.task_description = task_description

    def run(self):
        if self.input():
            self.solve()

    def __str__(self):
        return self.task_description

    def get_task_name(self):
        return self.task_name

    def input(self):
        try:
            n = int(input('Enter the natural number n: '))
            self.validate_args(n)
            values_dict = {'n': n}
            self.__dict__.update(values_dict)
            return values_dict
        except ValueError:
            print('Please, enter a number next time')
        except ValidationError:
            print('N must be > 0, be careful next time')

    @staticmethod
    def validate_args(n: int):
        if n <= 0:
            raise ValidationError('N must be > 0')

    @abstractmethod
    def solve(self):
        pass
