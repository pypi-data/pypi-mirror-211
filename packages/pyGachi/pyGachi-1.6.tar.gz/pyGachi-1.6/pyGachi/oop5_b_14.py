from datetime import datetime, timedelta

class Airplane:
    def __init__(self, destination, flight_number, departure_time):
        self.__destination = destination
        self.__flight_number = flight_number
        self.__departure_time = datetime.strptime(departure_time, "%H:%M")

    def get_destination(self):
        return self.__destination

    def get_flight_number(self):
        return self.__flight_number

    def get_departure_time(self):
        return self.__departure_time

    def __lt__(self, other):
        return self.__departure_time < other.get_departure_time()


class Airport:
    def __init__(self):
        self.__airplanes = []

    def add_airplane(self, airplane):
        self.__airplanes.append(airplane)

    def get_airplane_by_flight_number(self, flight_number):
        for airplane in self.__airplanes:
            if airplane.get_flight_number() == flight_number:
                return airplane
        return None

    def get_airplanes_within_hour(self, departure_time):
        search_time = datetime.strptime(departure_time, "%H:%M")
        limit_time = search_time + timedelta(hours=1)
        airplanes_within_hour = []
        for airplane in self.__airplanes:
            if search_time <= airplane.get_departure_time() <= limit_time:
                airplanes_within_hour.append(airplane)
        return airplanes_within_hour

    def get_airplanes_by_destination(self, destination):
        airplanes_by_destination = []
        for airplane in self.__airplanes:
            if airplane.get_destination() == destination:
                airplanes_by_destination.append(airplane)
        return airplanes_by_destination

    def sort_airplanes_by_departure_time(self):
        self.__airplanes.sort()

    def __str__(self):
        result = ""
        for airplane in self.__airplanes:
            result += f"Flight Number: {airplane.get_flight_number()}\n"
            result += f"Destination: {airplane.get_destination()}\n"
            result += f"Departure Time: {airplane.get_departure_time().strftime('%H:%M')}\n\n"
        return result


# Пример использования классов

# Создание объектов самолетов
airplane1 = Airplane("New York", "ABC123", "09:00")
airplane2 = Airplane("London", "DEF456", "10:30")
airplane3 = Airplane("Paris", "GHI789", "11:15")

# Создание объекта аэропорта
airport = Airport()

# Добавление самолетов в аэропорт
airport.add_airplane(airplane1)
airport.add_airplane(airplane2)
airport.add_airplane(airplane3)

# Получение информации о самолете по номеру рейса
flight_number = "DEF456"
airplane = airport.get_airplane_by_flight_number(flight_number)
if airplane is not None:
    print("Airplane Information:")
    print("Flight Number:", airplane.get_flight_number())
    print("Destination:", airplane.get_destination())
    print("Departure Time:", airplane.get_departure_time().strftime('%H:%M'))
else:
    print("No airplane found with the given flight number.")

# Получение информации о самолетах, отправляющихся в течение часа после введенного времени
departure_time = "10:00"
print("Airplanes Departing Within an Hour of", departure_time)
airplanes_within_hour = airport.get_airplanes_within_hour(departure_time)
for airplane in airplanes_within_hour:
    print("Flight Number:", airplane.get_flight_number())
    print("Destination:", airplane.get_destination())
    print("Departure Time:", airplane.get_departure_time().strftime('%H:%M'))

# Получение информации о самолетах, отправляющихся в заданный пункт назначения
destination = "Paris"
print("Airplanes Departing to", destination)
airplanes_by_destination = airport.get_airplanes_by_destination(destination)
for airplane in airplanes_by_destination:
    print("Flight Number:", airplane.get_flight_number())
    print("Destination:", airplane.get_destination())
    print("Departure Time:", airplane.get_departure_time().strftime('%H:%M'))

# Сортировка самолетов по времени отправления
airport.sort_airplanes_by_departure_time()

# Вывод всей информации о самолетах в аэропорту
print("All Airplanes in the Airport:")
print(airport)
