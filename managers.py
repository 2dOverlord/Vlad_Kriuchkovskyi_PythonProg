from transaction import TransactionCollection
from validator import ValidatorException
from memento import ConcreteMemento


class FileManager:
    def __init__(self, file_name, method):
        self.file_name = file_name
        self.method = method
        self.file_obj = open(file_name, method)
        self.file_obj.seek(0, 0)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.file_obj.close()

    def delete_data(self, obj_string):
        filedata = self.file_obj.read()
        self.file_obj.close()

        filedata = filedata.replace('{\n' + obj_string + '\n}', '')

        self.file_obj = open(self.file_name, 'w')
        self.file_obj.write(filedata)
        self.file_obj.close()

        self.file_obj = open(self.file_name, self.method)

    def append_object(self, obj_in_str):
        self.file_obj.write('\n{\n')
        self.file_obj.write(obj_in_str)
        self.file_obj.write('\n}')

    def get_all_data(self):
        self.file_obj.seek(0, 0)
        data = self.file_obj.read()
        return data


class CollectionManager:
    def __init__(self):
        self.collection = TransactionCollection()

    def save(self):
        """
        Saves the current state inside a memento.
        """
        try:
            self.file_name
            return ConcreteMemento(self.collection.container[:], self.file_name)
        except AttributeError:
            return ConcreteMemento(self.collection.container[:])

    def restore(self, memento) -> None:
        """
        Restores the Originator's state from a memento object.
        """

        self.collection.container, file_info = memento.get_state()

        if file_info:
            self.file_name = file_info['name']

            with open(self.file_name, 'w') as file:
                file.seek(0, 0)
                file.write(file_info['text'])

        print(f"Originator: My state has changed to previous")

    def get_all_objects_from_file(self):
        try:
            self.file_name
        except AttributeError:
            self.enter_file_name()

        try:
            with FileManager(self.file_name, 'r') as fm:
                data = fm.get_all_data()
        except FileNotFoundError:
            print('Please, input file name: ')
            del self.file_name
            return

        object_lists = []

        while data.find('\n') != -1:
            data = data.replace('\n', '')

        while data:
            object_list = []
            start = data.find('{')
            finish = data.find('}')

            object_string = data[start+1:finish]

            data = data.replace(data[start:finish+1], '')

            while object_string:
                start_in = object_string.find(':')
                finish_in = object_string.find(',')

                value = object_string[start_in + 1: finish_in]
                object_string = object_string.replace(object_string[:finish_in + 1], '')

                value.lstrip().rstrip()

                while value.find(' ') != -1:
                    value = value.replace(' ', '')
                object_list.append(value)

            object_lists.append(object_list)
        error_list = []
        for obj in object_lists:
            try:
                self.collection.append(obj)
            except ValidatorException as val_err:
                error_list.append(val_err)

        for val_err in error_list:
            with FileManager(self.file_name, 'r') as fm:
                object_id = val_err.obj_id
                count_lines = 0
                for line in fm.file_obj.readlines():
                    count_lines += 1
                    if f'id: {object_id}' in line:
                        print('Weve found error in file, here is the text of an error: ')
                        print(val_err)
                        print(f'id = {object_id}, field name = {val_err.field_name}, '
                              f'the string number is {count_lines}')

        save = input('Input yes, if you want to save all correct objects: ')

        if save != 'yes':
            for id in object_lists:
                self.collection.remove_by_id(int(id[0]))

    def search(self):
        pattern = input('Enter the search pattern: ')
        result = []

        for obj_dict in self.collection.get_data_in_dicts():
            for key, value in obj_dict.items():
                if str(value).find(pattern) != -1:
                    result.append(obj_dict['id'])
                    break
        print('Результати пошуку:')
        print('\n----------\n'.join([str(self.collection.find_by_id(id)) for id in result]))

    def sort(self):
        for obj in self.collection.sort():
            print(obj)

    def sort_by_key(self):
        try:
            fields = {'id', 'payer_name', 'card_number', 'month', 'year', 'cvc', 'payment_date', 'amount'}
            field_name = input('Введіть поле по якому хочете сортувати, доступні поля: ' + ' '.join(fields) + ': ')
            for obj in sorted(self.collection.container, key=lambda x: x.__getattribute__(field_name)):
                print(obj)
        except AttributeError:
            print('Ви ввели назву неіснуючого атрибуту')

    def input(self):
        input_fields = ['id', 'payer name', 'card number', 'month', 'year', 'cvc', 'payment date', 'amount']
        inputs = []

        for field in input_fields:
            inputs.append(input(f'Enter {field} value: ').replace(' ', ''))

        try:
            self.collection.append(inputs)
            print('Do you want to add new object to the file?')
            write = input('Enter yes if you want: ')
            if write == 'yes':
                try:
                    self.file_name
                except AttributeError:
                    self.enter_file_name()

                with FileManager(self.file_name, 'a') as fm:
                    obj = self.collection.find_by_id(int(inputs[0]))
                    fm.append_object(str(obj))

        except ValidatorException as val_err:
            print('\n' + 'Виникла помилка: ')
            print(val_err)
            print('\n')

    def change_file_name(self):
        self.enter_file_name(message='Добре, давайте оновимо назву файла')

    def enter_file_name(self, message='There is no file name in manager, please enter the file name: '):
        print(message)

        file_name = ''

        while not file_name[-4:] == '.txt':
            file_name = input('Введіть корректну назву файла: ')

        self.file_name = file_name

    def edit_by_id(self):
        fields = ['id', 'payer_name', 'card_number', 'month', 'year', 'cvc', 'payment_date', 'amount']
        field = input('Введіть назву поля для редактування: ' + ', '.join(fields) + ': ')
        value = input('Введіть нове значення: ')
        id = input('Введіть id об\'єкту: ')

        try:
            if not self.collection.edit_by_id(id, field_name=field, value=value):
                print('Об\'єкту з таким id або введеного поля немає')
                return
        except ValidatorException as err:
            print(err)

        try:
            self.file_name
        except AttributeError:
            self.enter_file_name()

        with FileManager(self.file_name, 'w') as fm:
            for obj in self.collection.container:
                fm.append_object(str(obj))

    def remove_by_id(self):
        id_ = input('Введіть id: ')
        try:
            id_ = int(id_)
            obj = self.collection.find_by_id(id_)
            if not obj:
                print('Нема об\'єкту з таким id')
                return
            object_string = str(obj)
            self.collection.remove_object(obj)
            try:
                with FileManager(self.file_name, 'r') as fm:
                    fm.delete_data(object_string)
            except AttributeError:
                pass

        except TypeError:
            print('Id must be an integer')

    def print_all(self):
        print('-'*15 + '\n')
        print('Виводимо на екран усі об\'єкти:')
        print(self.collection)

    def __str__(self):
        return str(self.collection)
