from validation import Validator


class FlightBooking:
    @Validator.validate_instance
    def __init__(self, avia_company, no_of_people, start_time, end_time, date, flight_number):
        self.avia_company = avia_company
        self.no_of_people = int(no_of_people)
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.flight_number = flight_number

    def get_flight_number(self):
        return self.flight_number

    def __str__(self):
        string = ''
        for key in self.__dict__:
            string += key + ':' + str(self.__dict__[key]) + '\n'
        return string