import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from prettytable import PrettyTable
import pickle
from pathlib import Path
from collections import UserDict
from datetime import datetime
import pickle
from .phone_book import ContactBook, Name, Contact
from .exception import input_error

p = Path("phone_data.bin")
phone_book = ContactBook()
if p.exists():
    with open("phone_data.bin", "rb") as file:
        phone_book.data = pickle.load(file)


def save_to_pickle():
    """ Save address book in pickle file"""

    with open("phone_data.bin", "wb") as fh:
        pickle.dump(phone_book.data, fh)


def say_hello(s=None):
    return "\nHow can I help you?\n"


def say_goodbye(s=None):
    return "\nGood bye!\n"


# Add new contact to address book
@input_error
def add_contact(value):

    name, *phones = value.lower().title().strip().split()
    name = Name(name.lower().title())

    if name.value not in phone_book:
        record = Contact(name, phones)
        phone_book.add_contact(record)
        if phones:
            for phone in phones:
                record.add_phone(phone)
        save_to_pickle()
        return f"\nContact {name.value.title()} was created.\n"
    else:
        return f"\nContact {name.value.title()} already exists.\n"


@input_error
def find_contact(name):
    contact = phone_book.get_contact(name)
    return contact

# The function displays all entries in the phone book with the 'show all' command.
@input_error
def show_all(s):

    if len(phone_book) == 0:
        return "\nPhone book is empty.\n"
    result = ''
    for record in phone_book.values():
       result += f"{record.contacts()}\n"
    return result


# Function for deleting a contact from the book.
@input_error
def remove_contact(name: str):

    record = phone_book[name.strip().lower().title()]
    phone_book.del_contact(record.name.value)
    save_to_pickle()
    return f"\nContact {name.title()} was removed.\n"


# Function for adding a contact's phone.
@input_error
def add_phone(value):

    name, phone = value.lower().strip().title().split()

    if name.title() in phone_book:
        phone_book[name.title()].add_phone(phone)
        save_to_pickle()
        return f"\nThe phone number for {name.title()} was recorded.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


# Function to delete a contact's phone.
@input_error
def remove_phone(value):

    name, phone = value.lower().title().strip().split()

    if name.title() in phone_book:
        phone_book[name.title()].delete_phone(phone)
        save_to_pickle()
        return f"\nPhone for {name.title()} was delete.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


# Function for replacing the phone of a contact.
@input_error
def change_ph(value: str):

    name, old_phone, new_phone = value.split()

    if name.strip().lower().title() in phone_book:
        phone_book[name.strip().lower().title()].change_phone(
            old_phone, new_phone)
        save_to_pickle()
    else:
        return f"\nContact {name.title()} does not exists\n"


# The function displays the phone number of the subscriber whose name was in the 'phone ...' command.
@input_error
def contact(name):

    if name.title() in phone_book:
        record = phone_book[name.title()]
        return record.contacts()
    else:
        return f"\nContact {name.title()} does not exist.\n"


# Function for adding an e-mail contact.
@input_error
def add_em(value):

    name, email = value.split()
    name = name.title()
    if name.title() in phone_book:
        phone_book[name.title()].add_email(email)
        save_to_pickle()
        return f"\nThe e-mail for {name.title()} was recorded.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


# Function for deleting an e-mail contact.
@input_error
def remove_em(value):

    name, email = value.split()
    name = name.title()
    email = email.lower()
    if name.title() in phone_book:
        phone_book[name.title()].delete_email(email)
        save_to_pickle()
        return f"\nThe e-mail for {name.title()} was delete.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


# Function for replacing e-mail contact.
@input_error
def change_em(value: str):

    name, old_em, new_em = value.split()

    if name.strip().lower().title() in phone_book:
        phone_book[name.strip().lower().title()].change_email(old_em, new_em)
        save_to_pickle()
        return f"\nThe e-mail for {name.title()} was changed.\n"
    else:
        return f"\nContact {name.title()} does not exists.\n"


# Function for adding a contact address.
@input_error
def add_adrs(value):

    name, address = value.split(" ", 1)
    name = name.title()
    if name.title() in phone_book:
        phone_book[name.title()].add_address(address)
        save_to_pickle()
        return f"\nThe address for {name.title()} was recorded.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


# Function for changing the address of a contact.
@input_error
def change_adrs(value):

    name, address = value.split(" ", 1)
    name = name.title()
    if name.strip().lower().title() in phone_book:
        phone_book[name.title()].add_address(address)
        save_to_pickle()
        return f"\nThe address for {name.title()} was changed.\n"
    else:
        return f"\nContact {name.title()} does not exists.\n"


# Function to delete contact address.
@input_error
def remove_adrs(value):

    name = value.lower().title().strip()
    if name.title() in phone_book:
        phone_book[name.title()].delete_address()
        save_to_pickle()
        return f"\nAddress for {name.title()} was delete.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


# A function to delete a contact's birthday.
@input_error
def remove_bd(value):

    name = value.lower().title().strip()

    if name.title() in phone_book:
        phone_book[name.title()].delete_birthday()
        save_to_pickle()
        return f"\nBirthday for {name.title()} was delete.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


# Function to add a contact's birthday to the book.
@input_error
def add_contact_birthday(value):

    name, birthday = value.lower().strip().split()

    if name.title() in phone_book:
        phone_book[name.title()].add_birthday(birthday)
        save_to_pickle()
        return f"\nThe Birthday for {name.title()} was recorded.\n"
    else:
        return f"\nContact {name.title()} does not exists.\n"


# The function displays the number of days until the contact's birthday.
@input_error
def days_to_bd(name):

    if name.title() in phone_book:
        if not phone_book[name.title()].birthday is None:
            days = phone_book[name.title()].days_to_birthday()
            return days
        else:
            return f"\n{name.title()}'s birthday is unknown.\n"
    else:
        return f"\nContact {name.title()} does not exists.\n"


# The function displays the list of birthday people for the period.
@input_error
def get_birthdays(value=None):

    if value.strip() == '':
        period = 7
    else:
        period = int(value.strip())
    return phone_book.get_birthdays_per_range(period)


# Function for changing the birthday of a contact.
@input_error
def change_bd(value):

    name, new_birthday = value.lower().strip().split()
    if name.title() in phone_book:
        phone_book[name.title()].delete_birthday()
        phone_book[name.title()].add_birthday(new_birthday)
        save_to_pickle()
        return f"\nBirthday for {name.title()} was changed.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"

# Search contact where there is 'text_to_search'.
@input_error
def search(text_to_search: str):

    return phone_book.search_contact(text_to_search)


def helps(value):
    rules = """LIST OF COMMANDS: \n
    1) to add new contact and one or more phones, write command: add contact <name>
    2) to remove contact, write command: remove contact <name>
    3) to add phone, write command: add phone <name> <one phone>
    4) to change phone, write command: change phone <name> <old phone> <new phone>
    5) to remove phone, write command: remove phone <name> <old phone>
    6) to add e-mail, write command: add email <name> <e-mail>
    7) to change e-mail, write command: change email <name> <new e-mail>
    8) to remove e-mail, write command: remove email <name>
    9) to add address, write command: add address <name> <address>
    10) to change address, write command: change address <name> <new address>
    11) to remove address, write command: remove address <name>
    12) to add birthday of contact, write command: add birthday <name> <dd/mm/yyyy>
    13) to remove birthday, write command: remove birthday <name>
    14) to change birthday, write command: change birthday <name> <d/m/yyyy>
    15) to see how many days to contact's birthday, write command: days to birthday <name>
    16) to see list of birthdays in period, write command: birthdays <number of days>
    17) to search contact, by name, write command: search contact <name>
    18) to see full record of contact, write: phone <name>
    19) to see all contacts, write command: show book
    20) to go to MENU, write command: menu . 
    21) to say hello, write command: hello
    22) to see help, write command: help
    """
    return rules


handlers = {
    "hello": say_hello,
    "menu": say_goodbye,
    "help": helps,
    "search contact": find_contact,
    "add contact": add_contact,
    "remove contact": remove_contact,
    "show book": show_all,
    "add phone": add_phone,
    "remove phone": remove_phone,
    "change phone": change_ph,
    "add email": add_em,
    "remove email": remove_em,
    "change email": change_em,
    "phone": contact,
    "add birthday": add_contact_birthday,
    "remove birthday": remove_bd,
    "change birthday": change_bd,
    "days to birthday": get_birthdays,
    "birthdays": get_birthdays,
    "change address": change_adrs,
    "remove address": remove_adrs,
    "add address": add_adrs
}

completer = NestedCompleter.from_nested_dict({
    "add": {
        "contact": {"<name> "},
        "phone": {"<name> <one phone>"},
        "email": {"<name> <e-mail>"},
        "address": {"<name> <address>"},
        "birthday": {"<name> <d/m/yyyy>"},
    },
    "remove": {
        "contact": {"<name>"},
        "phone": {"<name> <old phone>"},
        "email": {"<name>"},
        "address": {"<name>"},
        "birthday": {"<name>"},
    },
    "change": {
        "phone": {"<name> <old phone> <new phone>"},
        "email": {"<name> <new e-mail>"},
        "birthday": {"<name> <d/m/yyyy>"},
        "address": {"<name> <new address>"},
    },
    
    "phone": {"<name>"},
    "search": {
        "contact": {"<name>"},
    },

    "days to birthday": {"<name>"},
    "birthdays": {"<number of days>"},
    "hello": None,
    "help": None,
    "menu": None,
    "show book": None
})


def main():
    
    while True:
      
        command = prompt('(ADDRESS BOOK) Enter command >>> ', completer=completer)

        command = command.strip().lower()
        
        if command in ("menu"):
            say_goodbye()
            break
        else:
            match = False
            for key in handlers:
                if key in command:
                    match = True
                    print(handlers[key](command[len(key):].strip()))
                    break
            if not match:
                    print("\nEnter a valid command. Type 'help' for additional info\n")


if __name__ == "__main__":
    main()
