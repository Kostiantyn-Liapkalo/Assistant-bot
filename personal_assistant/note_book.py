import pickle


from collections import UserDict
from pathlib import Path
from prettytable import PrettyTable
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

########## COMMANDS ################

COMMANDS = ['add note', 'delete note', 'get by tag', 'get by title', 'get all', 'menu', 'edit note', 'help']
autocomplete_commands = WordCompleter(COMMANDS)


########## CLASSES ##################

class NoteBook(UserDict):

    def add_note(self, note):
        self.data.update({note.title: note})

    def get_note(self, title):
        note = self.data.get(title, None)
        return note

    def delete_note(self, title):
        deleted = self.data.pop(title)
        return deleted

    def get_notes_by_tag(self, tag):
        notes_list = self.data.values()
        notes = list(filter(lambda x: x.tag == tag, notes_list))
        return notes
    
    def get_all(self):
        notes_list = list(self.data.values())
        return notes_list

    def save_data_to_file(self):
        with open('notes_data.bin', 'wb') as file:
            pickle.dump(self.data, file)

    def retrieve_data_from_file(self):
            path = Path('notes_data.bin')
            if path.exists():
                with open('notes_data.bin', 'rb') as file:
                    is_file_empty = not bool(file.read()) 
                    if is_file_empty:
                        return
                    else:
                        file.seek(0)
                        deserialized = pickle.load(file)
                        self.data = deserialized 


class Note:
    def __init__(self):
        self._title = None
        self._tag = None
        self._text = None

    @property
    def title(self):
        return self._title
    
    @property
    def tag(self):
        return self._tag
    
    @property
    def text(self):
        return self._text

    @title.setter
    def title(self, title):
        if_exists = note_book.get_note(title)
        if if_exists:
            raise ValueError(f"Note with title {title} already exists")
        elif title == '':
            raise ValueError("Value should not be empty")
        elif len(title) > 20:
            raise ValueError("Title should not exceed 20 characters")
        else:
            self._title = title

    @tag.setter
    def tag(self, tag):
        if tag == '':
            raise ValueError("Value should not be empty")
        elif len(tag) > 20:
            raise ValueError("Title should not exceed 20 characters")
        else:
            self._tag = tag

    @text.setter
    def text(self, text):
        if text == '':
            raise ValueError("Value should not be empty")
        if len(text) > 250:
            raise ValueError("Title should not exceed 250 characters")
        else:
            self._text = text



class Tag:
    def __init__(self, value):
        self.value = value

class Title:
    def __init__(self, value):
        self.value = value

class Content:
    def __init__(self, value):
        self.value = value


##############  MODULE FUNCTIONS ################

chat_in_progress = True ##### RUNNING PROGRAM STATUS

note_book = NoteBook()


def input_error(func):
    def inner_func(args=None):
        try:
            if not args:
                result = func()
            else:
                result = func(args)
            return result
        except IndexError:
            print(
                "Assistant: Please, type ...")
        except ValueError as err:
            print(err.args[0])
            return None
    return inner_func


@input_error
def get_instructions(message):
    command_not_found = True

    for command in COMMANDS:
        if message.startswith(command):
            if command == "add note":
                args = create_note_object()
                return (command, args)
            args = message.replace(command, '').strip()
            command_not_found = False
            if command not in ["get all", "menu", "help"] and args == "":
                raise ValueError("Please enter required arguments: title/tag")
            return (command, args)
    if command_not_found:
        raise ValueError(
            f"Assistant: Please enter a valid command: {', '.join(COMMANDS)}")




def create_note_object():
    new_note = Note()
    while True:
        try:
            title = input("Enter a title: ").strip()
            new_note.title = title
        except ValueError as err:
            print(err.args[0])
            continue
        break
    while True:
        try:
            tag = input("Enter a tag: ").strip()
            new_note.tag = tag
        except ValueError as err:
            print(err.args[0])
            continue
        break
    while True:
        try:
            text = input("Type your note: ").strip()
            new_note.text = text
        except ValueError as err:
            print(err.args[0])
            continue
        break

    return [new_note]

def create_note_table(note):
    note_table = PrettyTable([f"Title: '{note.title}'   Tag: '{note.tag}'"])
    note_table.min_width = 50
    note_table.max_width = 50
    note_table.add_row([note.text])
    note_table.align = 'l'
    
    return note_table

@input_error
def add_note(args):
    [note] = args
    note_book.add_note(note)
    return f"Note with title '{note.title}' was successfully added"

@input_error
def get_note_by_title(args):
    title = args
    note = note_book.get_note(title)
    if not note:
        raise ValueError(f"Note with title '{title}' was not found")
    return f"\n{create_note_table(note)}\n"

@input_error
def get_notes_by_tag(args):
    tag = args
    notes = note_book.get_notes_by_tag(tag)
    if not len(notes):
        print(f"No notes holding '{tag}' tag were found")
        return
    result = ""
    for note in notes:
        table = create_note_table(note)
        num = notes.index(note) + 1
        result += f"\n   ----- {num} -----   \n{table}\n"
    return result

@input_error
def get_all_notes():
    notes = note_book.get_all()
    if not len(notes):
        print("There have been no notes added yet")
        return
    result = ""
    for note in notes:
        table = create_note_table(note)
        num = notes.index(note) + 1
        result += f"\n   ----- {num} -----   \n{table}\n"
    return result

@input_error
def edit_note(args):
    title = args
    note = note_book.get_note(title)
    if note:
        edited_text = prompt("Edit your note >>> ", default = note.text) 
        note.text = edited_text
        return "Note was successfully edited"
    else:
        return f"Note with title '{title}' was not found"

@input_error
def delete_note(args):
    title = args
    deleted = note_book.delete_note(title)
    print(f"Note with '{deleted.title}' was successfully deleted")

def greet():
    print("How can I help you with managing the notes?")


def terminate_assitant():
    global chat_in_progress 
    chat_in_progress = False

def show_help():
    print("""
    COMMANDS:
    1) add note: to add your new note
    2) get all: to get all notes
    3) get by title <title>: to get your note by title
    4) get by tag <tag>: to get the list of notes sharing the same tag value
    5) delete note <title>: to delete the note with a certain title
    6) edit note <title>: to edit the text of a note with a certain title
    7) menu: to go back to the main menu
    """)

def main():
    global chat_in_progress
    chat_in_progress = True
    while chat_in_progress:
        start_bot()

def start_bot():
    note_book.retrieve_data_from_file()
    message = (prompt("\n(NOTE BOOK) Enter command >>> ", completer=autocomplete_commands) or "no command")
    command_args = get_instructions(message)
    bot_message = None

    if not command_args:
        return

    command, args = command_args

    match command:
        case "add note":
            bot_message = add_note(args)
        case "get by title":
            bot_message = get_note_by_title(args)
        case 'get by tag':
            bot_message = get_notes_by_tag(args) 
        case 'get all':
            bot_message = get_all_notes()
        case 'edit note':
            bot_message = edit_note(args)   
        case 'delete note':
            bot_message = delete_note(args)
        case 'help':
            show_help()
        case "menu":
            terminate_assitant()

    if bot_message:
        print(bot_message)

    note_book.save_data_to_file()

##### MAIN PROCESS #####

if __name__ == "__main__":
    main()
