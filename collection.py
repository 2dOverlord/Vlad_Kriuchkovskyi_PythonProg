from flightBooking import FlightBooking


class AviaCompany:
    WIZZAIR = "Wizzair"
    RYANAIR = "Ryanair"
    SKYUP = "SkyUp"
    QATARAIRLINES = "QatarAirlines"


class Time:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute

    def __str__(self):
        return f'{self.hour}:{self.minute}'


class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def __eq__(self, other):
        return self.day == other.day and self.month == other.month and self.year == other.year

    def __str__(self):
        return f'{self.day}:{self.month}:{self.year}'

class FlightBookingCollection:
    def __init__(self):
        self.collection = []

    def read_from_file(self, fl_name):
        with open(fl_name) as f:
            lines = f.readlines()
        for line in lines:
            ready_line = line.split()
            self.add_object(ready_line)

    def add_object(self, args):
        avia_company, no_of_people, start_time, end_time, date, flight_number = args

        if avia_company == "Wizzair":
            avia_company = AviaCompany.WIZZAIR
        elif avia_company == "Ryanair":
            avia_company = AviaCompany.RYANAIR
        elif avia_company == "SkyUp":
            avia_company = AviaCompany.SKYUP
        elif avia_company == "QatarAirlines":
            avia_company = AviaCompany.QATARAIRLINES
        else:
            raise KeyError

        no_of_people = int(no_of_people)

        start_time = start_time.split(':')
        start_time = Time(int(start_time[0]), int(start_time[1]))

        end_time = end_time.split(':')
        end_time = Time(int(end_time[0]), int(end_time[1]))

        date = date.split(':')
        date = Date(int(date[0]), int(date[1]), int(date[2]))

        count = 1
        for obj_in in self.collection:
            if count > 300:
                print(f'Object with such flight number {flight_number} has already more than 300 passengers, sorry')
                continue
            if obj_in.flight_number == flight_number:
                count += 1
            if obj_in.date == date and obj_in.start_time != start_time and obj_in.end_time != end_time:
                print(f'Object with such time cant be added')
        obj = FlightBooking(avia_company, no_of_people, start_time, end_time, date, flight_number)
        self.collection.append(obj)

    def most_popular_hour(self):
        hours = {}
        for obj in self.collection:
            if obj.start_time.hour in hours:
                hours[obj.start_time.hour] += 1
            else:
                hours[obj.start_time.hour] = 1
        max_num = max(hours.values())
        for key in hours:
            if hours[key] == max_num:
                print(f'Start time: {key}, number = {max_num}')

    def most_popular_airline(self):
        airlines_dict = {
            "Wizzair": 0,
            "Ryanair": 0,
            "SkyUp": 0,
            "QatarAirlines": 0
        }

        for obj in self.collection:
            if obj.date.year == 2021:
                airlines_dict[obj.avia_company] += 1
        max_value = max(airlines_dict.values())
        name = None
        for value in airlines_dict:
            if airlines_dict[value] == max_value:
                name = value
        with open('max_company.txt', 'w') as f:
            f.write(f'{name}: {max_value}')

    def print_all(self):
        for obj in self.collection:
            print('-' * 8)
            print(obj)
            print('-' * 8)