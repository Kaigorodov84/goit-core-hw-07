from collections import UserDict
from datetime import datetime,  timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if len(value) !=0:   # перевірка чи ім'я не порожнє
            super().__init__(value)
        else:
            raise ValueError ("Enter your name")
        
	  
class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit(): #перевірка валідності номеру 
            super().__init__(value)
        else:
            raise ValueError("Enter a valid phone number")
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")   #перевірка формату дати та перетворення на об'єкт datetime 
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
   
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
                                            
    def add_phone(self, phone):          #Функція додавання номера телефону
        self.phones.append(Phone(phone))
                                                     
    def remove_phone(self, phone):  #Функція видалення номера телефону
        for phone in self.phones:
            if phone.value == phone:
                self.phones.remove(phone)
                                                 
    def edit_phone(self, old_phone, new_phone):   #Функція редагування номера телефону
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                print(f"Contact phone numbe {old_phone} edited on {new_phone} ")
                                                      
    def find_phone(self, phone):   #Функція знаходження номера телефону 
        return [p for p in self.phones if p.value == phone]
    
    def add_birthday(self, birthday):  #функція додавання дня народження до контакту
        if not self.birthday:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday already exists for this contact.")

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f', Birthday: {self.birthday}' if self.birthday else ''
        return f"Contact name: {self.name}, phones: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record): # Функція додавання запису 
        self.data[record.name.value] = record

    def find(self, name):  # Функція пошуку запису за ім'ям
        return self.data.get(name)

    def delete(self, name):  # Функція видалення запису за іменем
        if name in self.data:
            del self.data[name] 

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command."
        except KeyError:
            return "No such name found "
        except IndexError:
            return "Not found"
        except Exception as e:
            return f"Error: {e}"

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone = args
    if name not in book.data:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    else:
        return "Contact already exists."

@input_error
def change_contact(args, book):
    name, phone = args
    if name in book.data:
        book.data[name].remove_phone(phone)
        book.data[name].add_phone(phone)
        return "Contact updated."
    else:
        return "Contact not found."

@input_error    
def show_phone(args, book):
    name = args[0]
    return book[name] if name in book.keys() else "No such user"

@input_error
def show_all(args, book):
    s=''
    for key in book:
        s+=(f"{key:10} : {book[key]:10}\n")
    return s  

@input_error
def add_birthday(args, book):
    name, birthday = args
    if name in book.data:
        book.data[name].add_birthday(birthday)
        return "Birthday added to contact."
    else:
        raise ValueError("Record not found or date of birth not set.")

@input_error
def show_birthday(args, book):
    name = args[0]
    if name in book.data and book.data[name].birthday:
        return f" Birthday:{book.data[name].birthday.value}"
    elif name in book.data:
        return "Birthday not set."
    else:
        return "Contact not found."

@input_error
def birthdays(book):
    upcoming_birthdays = []
    current_day = datetime.now().date()
    next_week = current_day + timedelta(days=7)

    for record in book.data.values():
        if record.birthday:
            birthday_datetime = record.birthday.as_datetime().date()
            birthday_this_year = datetime(current_day.year, birthday_datetime.month, birthday_datetime.day).date()

            if birthday_this_year < current_day:
                birthday_this_year = datetime(current_day.year + 1, birthday_datetime.month, birthday_datetime.day).date()

            days_till_birthday = (birthday_this_year - current_day).days

            if 0 <= days_till_birthday <= 7:
                upcoming_birthdays.append({"name": record.name.value, "birthday": birthday_this_year.strftime("%d.%m.%Y")})

    return upcoming_birthdays

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
        