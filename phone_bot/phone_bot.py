from colorama import Fore, just_fix_windows_console

from decorators import input_error


class BreakError(Exception):
    pass


class ContinueError(Exception):
    pass


class ContactExist(Exception):
    pass


class ContactNotExist(Exception):
    pass


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    name, phone = args
    if name in contacts:
        raise ContactExist

    contacts[name] = phone
    return f"Contact {Fore.BLUE}{name}{Fore.RESET} added."


@input_error
def change_contact(args, contacts):
    name, phone = args

    if not name in contacts:
        raise ContactNotExist

    contacts[name] = phone
    return f"Contact {Fore.BLUE}{name}{Fore.RESET} updated."


@input_error
def delete_contact(args, contacts):
    name = args[0]

    del contacts[name]
    return f"Contact {Fore.RED}{name}{Fore.RESET} deleted."


@input_error
def show_contact(args, contacts):
    name = args[0]

    return f"{Fore.BLUE}{name}: {Fore.GREEN}{contacts[name]}{Fore.RESET}"


@input_error
def show_all_contacts(contacts, **qwargs):
    if not len(contacts):
        return "No contacts"

    showing_contacts = ""
    for name, phone in contacts.items():
        showing_contacts += f"{Fore.BLUE}{name}: {Fore.GREEN}{phone}{Fore.RESET}\n"
    return f"{"Phonebook:":-^100}\n{showing_contacts}"


@input_error
def hello(**qwargs):
    print("How can I help you?")


@input_error
def close(**qwargs):
    print("Good bye!")
    raise BreakError


@input_error
def show_commands(**qwargs):
    print(f"All commands: {', '.join(commands)}")


commands = {
    "hello": hello,
    "add": add_contact,
    "change": change_contact,
    "del": delete_contact,
    "phone": show_contact,
    "all": show_all_contacts,
    "help": show_commands,
    "close": close,
    "exit": close,
}


def main():

    contacts = {}
    print(f"""\n{"Welcome to the assistant bot!":*^100}
Commands list: {', '.join(commands)}
          """)
    while True:
        try:
            user_input = input("Enter a command: ")
        except KeyboardInterrupt:
            print("\nGood bye!")
            break

        if not user_input or not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        try:
            message = commands[command](args=args, contacts=contacts)
            if message:
                print(message)
        except KeyError:
            print("Unknown command")
        except BreakError:
            break
        except ContinueError:
            continue
        except ContactExist:
            print("Contact already exists. Rewrite it? (y/n): ")
            if input().lower() == "y":
                print(commands["change"](args=args, contacts=contacts))
            else:
                print("Contact not updated.")
        except ContactNotExist:
            print("Contact does not exist. Add it? (y/n): ")
            if input().lower() == "y":
                print(commands["add"](args=args, contacts=contacts))
            else:
                print("Contact not added.")


if __name__ == "__main__":
    just_fix_windows_console()
    main()
