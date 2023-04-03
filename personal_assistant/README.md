## Personal Assistant by PySoft

The project was elaborated with the purpose to improve personal planning routines in order to effectively manage all daily tasks.
It is exclusively based on the command line interface.

The following libraries were used: **autopep8,  beautifulsoup4, bs4, certifi, charset-normalizer, idna, prettytable, prompt-toolkit, pycodestyle,  requests soupsieve, urllib3, wcwidth**.


### Installation

Download package, unpack it and use next command to install it from unpacked folder:

```bush
pip install -e .
```

### Calling

Launch command line and use command **call-assistant**

___

### Description


Personal Assistant functionality:
In the beginning, you enter the main **MENU** interface where you will be asked to choose one of the tools:

- [x] NOTE BOOK
- [x] ADDRESS BOOK
- [x] FOLDER SORTER
- [x] WEATHER

To terminate the program type **exit**

**NOTE BOOK**

- [x] to add your new note: add note
- [x] to get all notes: get all
- [x] to get your note by title:  get by title <title>
- [x] to get the list of notes sharing the same tag value: get by tag <tag>
- [x] to delete the note with a certain title: delete note <title>
- [x] to edit the text of a note with a certain title: edit note <title>
- [x] to go back to the main menu:  menu


**ADDRESS BOOK**
- [x] to add new contact and one or more phones, write command: add contact <name>
- [x] to remove contact, write command: remove contact <name>
- [x] to add phone, write command: add phone <name> <one phone>
- [x] to change phone, write command: change phone <name> <old phone> <new phone>
- [x] to remove phone, write command: remove phone <name> <old phone>
- [x] to add e-mail, write command: add email <name> <e-mail>
- [x] to change e-mail, write command: change email <name> <new e-mail>
- [x] to remove e-mail, write command: remove email <name>
- [x] to add address, write command: add address <name> <address>
- [x] to change address, write command: change address <name> <new address>
- [x] to remove address, write command: remove address <name>
- [x] to add birthday of contact, write command: add birthday <name> <dd/mm/yyyy>
- [x] to remove birthday, write command: remove birthday <name>
- [x] to change birthday, write command: change birthday <name> <d/m/yyyy>
- [x] to see how many days to contact's birthday, write command: days to birthday <name>
- [x] to see list of birthdays in period, write command: birthdays <number of days>
- [x] to search contact, by name, write command: search contact <name>
- [x] to see full record of contact, write: phone <name>
- [x] to see all contacts, write command: show book
- [x] to go to MENU, write command: menu 
- [x] to say hello, write command: hello
- [x] to see help, write command: help


**FOLDER SORTER**
- [x] to sort a folder you should enter a path to it.
- [x] to go to MENU, write command: menu
- [x] supported formats for sorting:

```python
groups_of_format = {
        "images": ["JPEG", "PNG", "JPG", "SVG", "BMP"],
        "videos": ["AVI", "MP4", "MOV", "MKV"],
        "documents": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"],
        "audios": ["MP3", "OGG", "WAV", "AMR"],
        "archives": ["ZIP", "GZ", "TAR", "RAR"],
    }
```

**WEATHER**
- [x] by default weather forecast is set for Kyiv
- [x] to get the weather forecast type your city name
- [x] to go to MENU, write command: menu

___

### PySoft team:
<p> 
Dmytrii Shypilov (Team Lead) </p>
<p>Anton Akulenko (Scrum Master) </p>
<p>Kostiantyn Liapkalo (Developer) </p>
<p>Artur Mistiuk (Developer)</p>

