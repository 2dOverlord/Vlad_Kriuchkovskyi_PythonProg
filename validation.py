

class ValidatorException(BaseException):
    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message


class Validator:
    @staticmethod
    def validate_avia_company(avia_company):
        if avia_company not in ("Wizzair", "Ryanair", "SkyUp", "QatarAirlines"):
            raise ValidatorException("There is no such avia company")

    @staticmethod
    def validate_no_of_people(no_of_people):
        if int(no_of_people) > 300 or int(no_of_people) < 1:
            raise ValidatorException("No of people is not in range (1,300)")

    @staticmethod
    def validate_time(start_time, end_time):
        if start_time.hour > end_time.hour or start_time.hour > 23 or end_time.hour > 23:
            raise ValidatorException("Wrong start time/end time")
        elif start_time.hour == end_time.hour and start_time.minute > end_time.minute:
            raise ValidatorException("End time is less than start time")
        elif start_time.minute > 59 or end_time.minute > 59:
            raise ValidatorException("Wrong start time/end time")

    @staticmethod
    def validate_date(date):
        if date.day > 28 or date.day < 0 or date.month > 12 or date.month < 1:
            raise ValidatorException("Wrong date")

    @staticmethod
    def validate_flight_number(flight_number):
        #     (XX YYYY, X - літера, Y - цифра)
        if len(flight_number) != 6:
            raise ValidatorException('Wrong flight number')
        if not flight_number[:2].isalpha():
            raise ValidatorException('Wrong flight number')
        try:
            int(flight_number[2:])
        except ValueError:
            raise ValidatorException('Wrong flight number')

    @staticmethod
    def validate_instance(func):
        def wrapper(obj, avia_company, no_of_people, start_time, end_time, date, flight_number):
            Validator.validate_no_of_people(no_of_people)
            Validator.validate_time(start_time, end_time)
            Validator.validate_date(date)
            Validator.validate_flight_number(flight_number)
            func(obj, avia_company, no_of_people, start_time, end_time, date, flight_number)
        return wrapper