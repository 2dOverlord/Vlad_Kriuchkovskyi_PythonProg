from task_class import BaseTask
from custom_exceptions import ValidationError


class Pr1Task(BaseTask):
    def __init__(self):
        super().__init__(task_name='Pr1 11th variant',
                         task_description="""
                            Дано масив  натуральних чисел та число  (k<n). 
                            Знайти послідовних елементів масиву, середнє арифметичне яких є максимальним 
                            (вивести індекс першого елемента цієї послідовності і середнє арифметичне).
                            """)

    def input(self) -> dict:
        try:
            n = int(input('Enter the natural number n: '))
            array = []

            for _ in range(n):
                num = input(f"Enter element {_} of array(natural number): ")
                array.append(int(num))

            k = int(input("Enter k number(natural number, k < n): "))

            self.validate_args(n, array, k)
            values_dict = {
                'n': n,
                'array': array,
                'k': k
            }
            self.__dict__.update(values_dict)

            return values_dict
        except ValueError:
            print('Please, enter a number next time')
        except ValidationError as val_err:
            print(val_err)

    def solve(self) -> tuple:
        max_avg = 0
        index = -1

        for zero_index in range(self.n - self.k + 1):
            avg = sum(self.array[zero_index:zero_index + self.k]) / len(self.array[zero_index:zero_index + self.k])
            if avg > max_avg:
                index = zero_index
                max_avg = avg

        print(f'Index of the first element in a row is {index} and maximum arithmetical mean is {max_avg}')

        return max_avg, index

    @staticmethod
    def validate_args(n: int, array: list, k: int):
        if n <= 0:
            raise ValidationError('N must be > 0')
        if k >= n:
            raise ValidationError('k must be < n')
        for num in array:
            if num <= 0:
                raise ValidationError('nums in array must be > 0')


if __name__ == '__main__':
    while True:
        command = input('type exit if you want to stop code, if you want to run task type run: ')
        if command == 'run':
            task = Pr1Task()
            task.run()
        elif command == 'exit':
            exit()
        else:
            print('Unknown command')
