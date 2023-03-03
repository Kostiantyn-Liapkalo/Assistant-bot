from collections import UserDict
from datetime import datetime
import pickle
from pathlib import Path


# Exception for wrong length of the phone number
class WrongLengthPhoneError(Exception):
    pass


# Exception when a letter is in the phone number 
class LetterInPhoneError(Exception):
    pass


# Class for creating fields
class Field:

    def __init__(self, value):
        self._value = value.strip().lower().title()

    def __str__(self):
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value.strip().lower().title()


# Class for creating fields 'name'
class Name(Field):

    @Field.value.setter
    def value(self, value):
        self._value = value.strip().lower().title()


# Class for creating fields 'phone'
class Phone(Field):

    @staticmethod
    def sanitize_phone_number(phone):

        new_phone = str(phone).strip().removeprefix("+").replace(
            "(", "").replace(")", "").replace("-", "").replace(" ", "")
        try:
            new_phone = [str(int(i)) for i in new_phone]
        except ValueError:
            raise LetterInPhoneError("There is letter in the phone number!")

        else:
            new_phone = "".join(new_phone)
            if len(new_phone) == 12:
                return f"+{new_phone}"
            elif len(new_phone) == 10:
                return f"+38{new_phone}"
            else:
                raise WrongLengthPhoneError(
                    "Length of the phone's number is wrong")

    def __init__(self, value):
        self._value = Phone.sanitize_phone_number(value)

    @Field.value.setter
    def value(self, value):
        self._value = Phone.sanitize_phone_number(value)


# Class for creating fields 'birthday' 
class Birthday(datetime):

    @staticmethod
    def validate_date(year, month, day):
        try:
            birthday = datetime(year=year, month=month, day=day)
        except ValueError:
            print("Date is not correct\nPlease write date in format: yyyy-m-d")
        else:
            return str(birthday.date())

    def __init__(self, year, month, day):
        self.__birthday = self.validate_date(year, month, day)

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, year, month, day):
        self.__birthday = self.validate_date(year, month, day)


# Class for creating contacts
class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday=None):
        self.name = name
        if birthday is not None:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = None

        self.phones = []
        if phone:
            self.phones.append(phone)

    def days_to_bd(self):
        cur_date = datetime.now().date()
        cur_year = cur_date.year

        if self.birthday is not None:
            birthday = datetime.strptime(self.birthday, '%Y-%m-%d')
            this_year_birthday = datetime(cur_year, birthday.month,
                                          birthday.day).date()
            delta = this_year_birthday - cur_date
            if delta.days >= 0:
                return f"{self.name}'s birthday will be in {delta.days} days"
            else:
                next_year_birthday = datetime(cur_year + 1, birthday.month,
                                              birthday.day).date()
                delta = next_year_birthday - cur_date
                return f"{self.name}'s birthday will be in {delta.days} days"
        else:
            return f"{self.name}'s birthday is unknown"

    def add_birthday(self, year, month, day):
        self.birthday = Birthday.validate_date(int(year), int(month), int(day))

    def add_phone(self, phone):
        phone = Phone(phone)
        if phone:
            lst = [phone.value for phone in self.phones]
            if phone.value not in lst:
                self.phones.append(phone)
                return "Phone was added"
        else:
            raise ValueError("Phone number is not correct")

    def change_phone(self, old_phone, new_phone):
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)

        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return "phone was changed"

    def delete_phone(self, old_phone):
        old_phone = Phone(old_phone)
        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)

    def get_contact(self):
        phones = ", ".join([str(p) for p in self.phones])
        return {
            "name": str(self.name.value),
            "phone": phones,
            "birthday": self.birthday
        }


# Class for creating addressbooks
class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        name = name.lower().title()
        if name in self.data:
            self.data.pop(name)

    def all_records(self):
        return {key: value.get_contact() for key, value in self.data.items()}

    def iterator(self):
        for record in self.data.values():
            yield record.get_contact()


p = Path("address_book.bin")
address_book = AddressBook()
if p.exists():
    with open("address_book.bin", "rb") as file:
        address_book.data = pickle.load(file)
