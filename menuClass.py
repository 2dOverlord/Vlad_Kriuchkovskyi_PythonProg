from validation import ValidatorException
from collection import FlightBookingCollection


class Menu:
    def __init__(self):
        self.collection = FlightBookingCollection()
        self.commands = {
            'read': self.read_from_file,
            'add': self.add_object,
            'popular hours': self.collection.most_popular_hour,
            'max_value': self.collection.most_popular_airline,
            'print all': self.collection.print_all,
            'exit': exit,
        }

    def read_from_file(self):
        file_name = input('Enter the file name: ')
        self.collection.read_from_file(file_name)

    def add_object(self):
        print('Please enter date in form of day:month:year and enter any time in form of hour:minute')
        args = ["avia_company", "no_of_people", "start_time", "end_time", "date", "flight_number"]
        input_args = []
        for arg in args:
            input_args.append(input(f'Enter the {arg}: '))
        self.collection.add_object(input_args)

    def __call__(self, *args, **kwargs):
        while True:
            try:
                command_key = input('Please, enter one of this commands| ' + ', '.join(self.commands.keys()) + ' |: ')
                self.commands[command_key]()
            except ValidatorException as err:
                print(err)
            except KeyError:
                print('There is no such command')
            except Exception:
                print('Smth gone wrong')