import pickle
import re
from Classes import address_book, Record, Name
from exceptions import input_error


# Save address book in pickle file
def save_to_pickle():

    with open("address_book.bin", "wb") as file:
        pickle.dump(address_book.data, file)


# Search contact where there is 'text' in the fields: name and phone
@input_error
def search(value: str):

    for record in address_book:
        contact = address_book[record]
        for text in contact.get_contact().values():
            if text != None:
                if re.findall(value, text):
                    print(address_book[record].get_contact())
                    break


def say_hello(s):
    return "How can I help you?"


def say_goodbye(s=None):
    return "Good bye!"


# Add new contact to address book
@input_error
def add_contact(value):

    name, *phones = value.lower().strip().split()
    name = Name(name.lower().title())

    if not name.value in address_book:
        record = Record(name)
        address_book.add_record(record)
        for phone in phones:
            record.add_phone(phone)
            save_to_pickle()
        return f"Contact {name.value.title()} was created"
    else:
        return f"Contact {name.value.title()} already exists"


@input_error
def add_phone(value):
    name, phone = value.lower().strip().split()

    if name.title() in address_book:
        address_book[name.title()].add_phone(phone)
        save_to_pickle()
        return f"The phone number for {name.title()} was recorded"
    else:
        return f"Contact {name.title()} does not exist"


@input_error
def remove_phone(value):
    name, phone = value.lower().strip().split()

    if name.title() in address_book:
        address_book[name.title()].delete_phone(phone)
        save_to_pickle()
        return f"Phone for {name.title()} was delete"
    else:
        return f"Contact {name.title()} does not exist"


@input_error
def add_contact_birthday(value):
    name, birthday = value.lower().strip().split()
    birthday = tuple(birthday.split("-"))

    if name.title() in address_book:
        address_book[name.title()].add_birthday(*birthday)
        save_to_pickle()
        return f"The Birthday for {name.title()} was recorded"
    else:
        return f"Contact {name.title()} does not exists"


@input_error
def days_to_birthday(name):
    if name.title() in address_book:
        if not address_book[name.title()].birthday is None:
            days = address_book[name.title()].days_to_bd()
            return days
        else:
            return f"{name.title()}'s birthday is unknown"
    else:
        return f"Contact {name.title()} does not exists"


@input_error
def change_ph(value: str):
    name, old_phone, new_phone = value.split()

    if name.strip().lower().title() in address_book:
        address_book[name.strip().lower().title()].change_phone(
            old_phone, new_phone)
        save_to_pickle()
    else:
        return f"Contact {name.title()} does not exists"


@input_error
def remove_contact(name: str):
    record = address_book[name.strip().lower().title()]
    address_book.remove_record(record.name.value)
    save_to_pickle()
    return f"Contact {name.title()} was removed"


# The function displays the phone number of the subscriber whose name was in the command 'phone'
@input_error
def contact(name):

    if name.title() in address_book:
        record = address_book[name.title()]
        return record.get_contact()
    else:
        return f"Contact {name.title()} does not exist"


# The function displays all entries in the phone book with the 'show all' command
def show_all(s):
    
    if len(address_book) == 0:
        return "Phone book is empty"
    for record in address_book.values():
        print(record.get_contact())


def help(value):
    rules = """List of commands:
    1) to add new contact and one or more phones, write command: add {name} {phone number} {phone number} {phone number}
    2) to remove contact, write command: remove contact {name}

    3) to add phone, write command: add phone {name} {one phone}
    4) to change phone, write command: change phone {name} {old phone} {new phone}
    5) to remove phone, write command: remove phone {name} {old phone}

    6) to add birthday of contact, write command: add birthday {name} {yyyy-m-d}
    7) to see how many days to contact's birthday, write command: days to birthday {name}

    8) to search contact, where is 'text', write command: search {text}
    9) to see full record of contact, write: phone {name}
    10) to see all contacts, write command: show all
    11) to say goodbye, write one of these commands: good bye / close / exit
    12) to say hello, write command: hello
    13) to see help, write command: help
    """
    return rules


# A dictionary where keys are keywords in commands, and values ​​are functions that are called by these commands
commands = {
    "remove contact": remove_contact,
    "add phone": add_phone,
    "change phone": change_ph,
    "remove phone": remove_phone,
    "add birthday": add_contact_birthday,
    "days to birthday": days_to_birthday,
    "add": add_contact,
    "search": search,
    "phone": contact,
    "show all": show_all,
    "hello": say_hello,
    "good bye": say_goodbye,
    "close": say_goodbye,
    "exit": say_goodbye,
    "help": help
}


@input_error
def main():
    while True:
        command = input("Enter command: ")

        if command.lower() in (".", "close", "exit", "good bye"):
            say_goodbye()
            break

        for key in commands:
            if command.lower().strip().startswith(key):
                print(commands[key](command[len(key):].strip()))
                break


if __name__ == "__main__":
    main()
    save_to_pickle()
