from collections import UserDict
import datetime as dt
from datetime import datetime as dtdt

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
            self.value = dtdt.strptime(value, "%d.%m.%Y")   #перевірка формату дати та перетворення на об'єкт datetime 
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

def parse_input(user_input):         #функція розбивання введеного рядка на слова (використовує пробіл як розділювач )
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    if len(args) != 2:
        return "Invalid command. Usage: add [name] [phone]"
    
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

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
def show_all(book):
    if not book.data:
        return "No contacts found."
    
    for name, record in book.data.items():
        print(f"{name}: {'; '.join(str(phone) for phone in record.phones)}")
    return "" 

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
    tdate=dtdt.today().date() # беремо сьогоднішню дату
    birthdays=[] # створюємо список для результатів
    for user in book: # перебираємо користувачів
        bdate=user["birthday"].replace("-","") # отримуємо дату народження людини у вигляді числового  рядка
        bdate=str(tdate.year)+bdate[4:] # Замінюємо рік на поточний
        bdate=dtdt.strptime(bdate, "%Y.%m.%d").date() # перетворюємо дату народження в об’єкт date
        week_day=bdate.isoweekday() # Отримуємо день тижня (1-7)
        days_between=(bdate-tdate).days # рахуємо різницю між зараз і днем народження цьогоріч у днях
        if 0<=days_between<7: # якщо день народження протягом 7 днів від сьогодні
            if week_day<6: #  якщо пн-пт
                birthdays.append({'name':user[book], 'birthday':bdate.strftime("%Y.%m.%d")}) 
                # Додаємо запис у список.
            else:
                if (bdate+dt.timedelta(days=1)).weekday()==0:# якщо неділя
                    birthdays.append({'name':user[book], 'birthday':(bdate+dt.timedelta(days=1)).strftime("%Y.%m.%d")})
                    #Переносимо на понеділок. Додаємо запис у список.
                elif (bdate+dt.timedelta(days=2)).weekday()==0: #якщо субота
                    birthdays.append({'name':user[book], 'birthday':(bdate+dt.timedelta(days=2)).strftime("%Y.%m.%d")})
                    #Переносимо на понеділок. Додаємо запис у список.
    return birthdays

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
        