from collections import UserDict
from typing import List


class Field:
    def __init__(self, value) -> None:
        self.value = value.title()

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    def __init__(self, *args):
        super().__init__(*args)


class Phone(Field):
    def __init__(self, *args):
        super().__init__(*args)


class Record:
    def __init__(self, name: Name, phones: List[Phone] = []) -> None:
        self.name = name
        self.phones = phones

    def add_phone(self, phone) -> None:
        self.phones.append(phone)

    def change_phone(self, phone, new_phone) -> None:
        self.phones.remove(phone)
        self.phones.append(new_phone)

    def del_phone(self, phone) -> None:
        self.phones.remove(phone)

    def __str__(self) -> str:
        return f'Contact {self.name}: Phones {self.phones}'


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record


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
    name, phone = Name(args[0]), Phone(args[1])
    if name.value in notebook:
        notebook[name.value].add_phone(phone.value)
        return f"Contact {name.value} has added successfully."
    else:
        notebook[name.value] = Record(name, [phone.value])
        return f"Contact {name.value} has added successfully."


@input_error
def change_number(*args):
    name, phone, new_phone = Name(args[0]), Phone(args[1]), Phone(args[2])
    notebook[name.value].change_phone(phone.value, new_phone.value)
    return f"Contact {name.value} has changed successfully."


@input_error
def del_number(*args):
    name, phone = Name(args[0]), Phone(args[1])
    notebook[name.value].del_phone(phone.value)
    return f"Contact {name.value} has deleted successfully."


@input_error
def print_phone(*args):
    name = Name(args[0])
    return notebook[name.value]


def show_all(*args):
    return "\n".join([f"{k.title()}: {v}" for k, v in notebook.items()]) if len(notebook) > 0 else 'Contacts are empty'


all_commands = {
    greeting: ["hello", "hi"],
    add_contact: ["add", "new", "+"],
    change_number: ["change", ],
    print_phone: ["phone", "number"],
    show_all: ["show all", "show"],
    to_exit: ["good bye", "close", "exit", ".", "bye"],
    del_number: ["del", "delete", "-"]
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
