from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        if not (isinstance(self.value, str) and len(self.value) == 10 and self.value.isdigit()):
            raise ValueError("Invalid phone number format")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if str(phone) == old_phone:
                phone.value = new_phone
                break
        else:
            raise ValueError("Phone number does not exist in the record")

    def get_phones(self):
        return [str(phone) for phone in self.phones]

    def find_phone(self, phone):
        found_phones = [p for p in self.phones if str(p) == phone]
        return found_phones[0] if found_phones else None

    def __str__(self):
        return f"Contact name: {self.name}, phones: {', '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"
    return wrapper


contacts = AddressBook()


@input_error
def add_contact(name, phone):
    contact = contacts.find(name)
    if contact:
        contact.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
    return f"Contact {name} added with phone {phone}"


@input_error
def delete_contact(name):
    contact = contacts.find(name)
    if contact:
        contacts.delete(name)
        return f"Contact {name} deleted"
    else:
        return f"Contact {name} not found"

@input_error
def get_phone(name):
    contact = contacts.find(name)
    if contact and contact.phones:
        return f"Phone numbers for {name}: {', '.join(contact.get_phones())}"
    else:
        raise ValueError(f"Contact {name} not found")
@input_error
def change_phone(name, new_phone):
    contact = contacts.find(name)
    if contact:
        contact.edit_phone(contact.phones[0].value, new_phone)
    else:
        raise ValueError(f"Contact {name} not found")


@input_error
def get_phone(name):
    contact = contacts.find(name)
    if contact and contact.phones:
        return f"Phone number for {name}: {contact.phones[0].value}"
    else:
        raise ValueError(f"Contact {name} not found")


@input_error
def show_all():
    return str(contacts)


def main():
    while True:
        command = input("Enter command: ").lower()

        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            _, name, phone = command.split()
            print(add_contact(name, phone))
        elif command.startswith("delete"):
            _, name = command.split()
            print(delete_contact(name))
        elif command.startswith("change"):
            _, name, new_phone = command.split()
            print(change_phone(name, new_phone))
        elif command.startswith("phone"):
            _, name = command.split()
            print(get_phone(name))
        elif command == "show all":
            print(show_all())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()