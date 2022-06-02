from collections import UserDict
from typing import List, Tuple


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name: Name, phones: List[Phone] = []) -> None:
        self.name = name
        self.phones = phones

    def add_phone(self, phone: Phone) -> Phone | None:
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return phone

    def del_phone(self, phone: Phone) -> Phone | None:
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)
                return p

    def change_phone(self, phone, new_phone) -> tuple[Phone, Phone] | None:
        if self.del_phone(phone):
            self.add_phone(new_phone)
            return phone, new_phone

    def __str__(self) -> str:
        return f'Phones {", ".join([p.value for p in self.phones])}'


class AddressBook(UserDict):
    def add_record(self, record: Record) -> Record | None:
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
            return record

    def del_record(self, key: str) -> Record | None:
        rec = self.data.get(key)
        if rec:
            self.data.pop(key)
            return rec


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Please enter the contact like this:\nName: number"
        except KeyError:
            return "This contact doesn't exist."
        except ValueError:
            return "Invalid command entered."

    return inner


def greeting(*args):
    return "How can I help you?"


def to_exit(*args):
    return "Good bye"


notebook = AddressBook()


@input_error
def add_contact(*args):
    rec = Record(Name(args[0]), [Phone(args[1])])
    if notebook.add_record(rec):
        return f"Contact {rec.name.value} has added successfully."
    else:
        return f'{rec.name.value} contact is in the notebook already.'


@input_error
def change_number(*args):
    rec = notebook.get(args[0])
    if rec:
        rec.change_phone(Phone(args[1]), Phone(args[2]))
        return f'Contact {rec.name.value} has changed successfully.'
    return f'Contact, with name {args[0]} not in notebook.'


@input_error
def del_number(*args):
    rec = notebook.get(args[0])
    if rec:
        rec.del_phone(Phone(args[1]))
        return f'Contact {args[1]} has deleted successfully from contact {rec.name.value}.'
    return f'Contact, with name {args[0]} not in notebook.'


@input_error
def print_phone(*args):
    return notebook[args[0]]


@input_error
def del_contact(*args):
    rec = notebook.del_record(args[0])
    if rec:
        return f'Contact {rec.name.value} has deleted successfully.'
    return f'Contact, with name {args[0]} not in notebook.'


def show_all(*args):
    return "\n".join([f"{k.title()}: {v}" for k, v in notebook.items()]) if len(notebook) > 0 else 'Contacts are empty'


all_commands = {
    greeting: ["hello", "hi"],
    add_contact: ["add", "new", "+"],
    change_number: ["change", ],
    print_phone: ["phone", "number"],
    show_all: ["show all", "show"],
    to_exit: ["good bye", "close", "exit", ".", "bye"],
    del_number: ["del", "delete", "-"],
    del_contact: ["remove", ],
}


def command_parser(user_input: str):
    for key, value in all_commands.items():
        for i in value:
            if user_input.lower().startswith(i.lower()):
                return key, user_input[len(i):].strip().split()


def main():
    while True:
        user_input = input(">>> ")
        command, parser_data = command_parser(user_input)
        print(command(*parser_data))
        if command is to_exit:
            break


if __name__ == "__main__":
    main()
