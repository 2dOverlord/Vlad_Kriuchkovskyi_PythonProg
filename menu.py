from managers import CollectionManager
from memento import Caretaker

class Command:
    def __init__(self, name, description=''):
        self.name = name
        self.description = description

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Menu:
    def __init__(self):
        self.manager = CollectionManager()
        self.caretaker = Caretaker(self.manager)
        self.caretaker.backup()
        self.start_commands = {
            Command('print all', 'Print all objects'): self.manager.print_all,
            Command('input', 'Add object or objects to collection'): self.input,
            Command('change file', 'Change txt file name'): self.manager.change_file_name,
            Command('find', 'Search menu'): self.search,
            Command('sort', 'Sort menu'): self.sort,
            Command('edit', 'Edit an object by id'): self.manager.edit_by_id,
            Command('remove', 'Remove an object by id'): self.manager.remove_by_id,
            Command('undo', 'Undo the previous command'): self.caretaker.undo,
            Command('redo', 'Redo the previous command'): self.caretaker.redo,
            Command('exit', 'Exit from program'): exit,
        }

        self.input_commands = {
            Command('console input', 'Enter object from console'): self.manager.input,
            Command('file input', 'Enter objects from txt file'): self.manager.get_all_objects_from_file,
        }

        self.search_commands = {
            Command('pattern search', 'Find pattern searching in all fields'): self.manager.search,
        }

        self.sort_commands = {
            Command('sort by many', 'Sorting by all fields'): self.manager.sort,
            Command('sort by field', 'Sorting by certain field'): self.manager.sort_by_key,
        }

    def __call__(self, *args, **kwargs):
        while True:
            print('-'*15)
            print('This is programm menu, please choose one option from this commands:')
            for command in self.start_commands:
                print(f'{command.name}: {command.description}\n')
            print('-'*15 + '\n')
            input_command = input('Enter command name: ')
            try:
                self.start_commands[Command(input_command)]()
                if input_command not in ('print all', 'find', 'exit', 'undo', 'redo', 'return'):
                    self.caretaker.backup()
            except KeyError:
                print('There is no such command\n')

    def input(self):
        self.run_additional_menu('Input menu:', self.input_commands)

    def search(self):
        self.run_additional_menu('Search menu:', self.search_commands)

    def sort(self):
        self.run_additional_menu('Sort menu: ', self.sort_commands)

    def run_additional_menu(self, start_message, add_commands):
        while True:
            print('-'*15)
            print(start_message)
            for command in add_commands:
                print(f'{command.name}: {command.description}\n')
            print('return: Return to main menu')
            print('-' * 15 + '\n')
            input_command = input('Enter command name: ')
            try:
                if input_command == 'return':
                    break
                add_commands[Command(input_command)]()
            except KeyError:
                print('Ви ввели неіснуючу команду\n')
