from datetime import date, timedelta

class Record:
    def __init__(self, last_name, first_name, phone_number, birth_date):
        self.__last_name = last_name
        self.__first_name = first_name
        self.__phone_number = phone_number
        self.__birth_date = birth_date

    def get_last_name(self):
        return self.__last_name

    def get_first_name(self):
        return self.__first_name

    def get_phone_number(self):
        return self.__phone_number

    def get_birth_date(self):
        return self.__birth_date

    def is_birthday_today(self):
        today = date.today()
        return self.__birth_date.day == today.day and self.__birth_date.month == today.month

    def is_birthday_next_week(self):
        today = date.today()
        next_week = today + timedelta(weeks=1)
        return today <= self.__birth_date < next_week

    def has_phone_number_prefix(self, prefix):
        return self.__phone_number.startswith(prefix)


class AddressBook:
    def __init__(self):
        self.__records = []

    def add_record(self, record):
        self.__records.append(record)

    def find_record_by_phone_number(self, phone_number):
        for record in self.__records:
            if record.get_phone_number() == phone_number:
                return record
        return None

    def find_birthdays_today(self):
        birthdays_today = []
        today = date.today()
        for record in self.__records:
            if record.get_birth_date().day == today.day and record.get_birth_date().month == today.month:
                birthdays_today.append(record)
        return birthdays_today

    def find_birthdays_next_week(self):
        birthdays_next_week = []
        today = date.today()
        next_week = today + timedelta(weeks=1)
        for record in self.__records:
            if today <= record.get_birth_date() < next_week:
                birthdays_next_week.append(record)
        return birthdays_next_week

    def find_records_by_phone_prefix(self, prefix):
        matching_records = []
        for record in self.__records:
            if record.has_phone_number_prefix(prefix):
                matching_records.append(record)
        return matching_records


# Пример использования классов

# Создание объектов записей
record1 = Record("Иванов", "Иван", "123456789", date(1990, 5, 10))
record2 = Record("Петров", "Петр", "987654321", date(1985, 8, 15))
record3 = Record("Сидоров", "Алексей", "567890123", date(1992, 12, 20))

# Создание объекта записной книжки
address_book = AddressBook()

# Добавление записей в записную книжку
address_book.add_record(record1)
address_book.add_record(record2)
address_book.add_record(record3)

# Поиск записи по номеру телефона
phone_number = "987654321"
found_record = address_book.find_record_by_phone_number(phone_number)
if found_record is not None:
    print("Record Found:")
    print("Last Name:", found_record.get_last_name())
    print("First Name:", found_record.get_first_name())
    print("Phone Number:", found_record.get_phone_number())
    print("Birth Date:", found_record.get_birth_date().strftime('%d-%m-%Y'))
else:
    print("Record Not Found")

# Поиск дней рождения сегодня
birthdays_today = address_book.find_birthdays_today()
if len(birthdays_today) > 0:
    print("\nBirthdays Today:")
    for record in birthdays_today:
        print(record.get_last_name(), record.get_first_name())
else:
    print("\nNo Birthdays Today")

# Поиск дней рождения на следующей неделе
birthdays_next_week = address_book.find_birthdays_next_week()
if len(birthdays_next_week) > 0:
    print("\nBirthdays Next Week:")
    for record in birthdays_next_week:
        print(record.get_last_name(), record.get_first_name())
else:
    print("\nNo Birthdays Next Week")

# Поиск записей с номерами телефонов, начинающихся с заданного префикса
phone_prefix = "567"
matching_records = address_book.find_records_by_phone_prefix(phone_prefix)
if len(matching_records) > 0:
    print("\nRecords with Phone Number Prefix", phone_prefix)
    for record in matching_records:
        print("Last Name:", record.get_last_name())
        print("First Name:", record.get_first_name())
        print("Phone Number:", record.get_phone_number())
else:
    print("\nNo Records Found with Phone Number Prefix", phone_prefix)