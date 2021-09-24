from task_class import BaseTask
from custom_exceptions import ValidationError


class Pr2Task(BaseTask):
    def __init__(self):
        super().__init__(task_name='Pr2 11th variant',
                         task_description="""
                            Дані цілі числа a1,...,am і цілочисельна квадратна матриця порядку n. 
                            Замінити нулями в матриці ті елементи з парною сумою індексів, 
                            для яких є рівні елементи серед a1,...,am
                            """)

    def input(self):
        try:
            m = int(input('Enter natural number m: '))
            m_numbers = []

            for _ in range(m):
                m_numbers.append(int(input(f"Enter element {_} of array: ")))

            n = int(input('Enter natural number n: '))
            n_array = []

            for i in range(n):
                n_temp_array = []
                for j in range(n):
                    n_temp_array.append((int(input(f'Enter element {i}, {j}: '))))
                n_array.append(n_temp_array)
            self.validate_args(m, n)

            values_dict = {
                'm': m,
                'm_numbers': m_numbers,
                'n': n,
                'n_array': n_array,
            }
            self.__dict__.update(values_dict)

            return values_dict
        except ValueError:
            print('Please, enter a number next time')
        except ValidationError as val_err:
            print(val_err)

    def solve(self):
        for i in range(self.n):
            for j in range(self.n):
                if (i + j) % 2 == 0 and self.n_array[i][j] in self.m_numbers:
                    self.n_array[i][j] = 0

        for i in range(self.n):
            print(' '.join([str(j) for j in self.n_array[i]]))

        return self.n_array[:]

    @staticmethod
    def validate_args(m: int, n: int):
        if m <= 0:
            raise ValidationError('m must be > 0')
        if n <= 0:
            raise ValidationError('n must be > 0')
