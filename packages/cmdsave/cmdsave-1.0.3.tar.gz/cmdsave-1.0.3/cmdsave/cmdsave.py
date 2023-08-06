import argparse
import csv
import os
import time
import keyboard
import pyperclip
import subprocess


def save_command(args):
    command = input("Enter the command you want to save: ")
    name = input("Enter a name to save it for easy reference: ")

    with open('commands.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, command])

    print("\nCommand saved successfully.")


def display_commands(args):
    if not os.path.isfile('commands.csv'):
        print('No commands found.')
        return

    with open('commands.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        commands = list(reader)

    selected_index = 0
    num_commands = len(commands)

    while True:
        os.system('cls')

        print("Use arrow keys to navigate the list.\nPress Enter to select a command and copy it to the clipboard.\n")

        for i, command in enumerate(commands):
            if i == selected_index:
                print(
                    f"[{i+1}] \033[7m{command[0]}\033[0m: {command[1]}")
            else:
                print(f"[{i+1}] {command[0]}: {command[1]}")

        time.sleep(0.1)
        key = keyboard.read_key(suppress=True)

        if key == 'up':
            selected_index = (selected_index - 1) % num_commands
        elif key == 'down':
            selected_index = (selected_index + 1) % num_commands
        elif key == 'enter':
            selected_command = commands[selected_index][1]
            pyperclip.copy(selected_command)
            print(
                f"\nSelected command copied to clipboard.\n{selected_command}")
            break


def delete_command(args):
    if not os.path.isfile('commands.csv'):
        print('No commands found.')
        return

    with open('commands.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        commands = list(reader)

    selected_index = 0
    num_commands = len(commands)

    while True:
        os.system('cls')

        print("Use arrow keys to navigate the list.\nPress Enter to select a command to delete.\n")

        for i, command in enumerate(commands):
            if i == selected_index:
                print(
                    f"[{i+1}] \033[7m{command[0]}\033[0m: {command[1]}")
            else:
                print(f"[{i+1}] {command[0]}: {command[1]}")

        time.sleep(0.1)
        key = keyboard.read_key(suppress=True)

        if key == 'up':
            selected_index = (selected_index - 1) % num_commands
        elif key == 'down':
            selected_index = (selected_index + 1) % num_commands
        elif key == 'enter':
            selected_command = commands[selected_index]
            delete_confirmation = input(
                f"\nAre you sure you want to delete the command?\n'{selected_command[0]}: {selected_command[1]}'\n(Y/N): ")

            if delete_confirmation.lower() == 'y':
                with open('commands.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for i, command in enumerate(commands):
                        if i != selected_index:
                            writer.writerow(command)
                print("\nCommand deleted successfully.")
            else:
                print("\nDeletion canceled.")
            break


def edit_csv_file(args):
    csv_file = os.path.abspath('commands.csv')
    subprocess.Popen(['notepad.exe', csv_file])


def main():
    parser = argparse.ArgumentParser(description='Save CMDs')
    subparsers = parser.add_subparsers(dest='command', metavar='command')

    save_parser = subparsers.add_parser('save', help='Save a command')
    save_parser.set_defaults(func=save_command)

    list_parser = subparsers.add_parser('list', help='List saved commands')
    list_parser.set_defaults(func=display_commands)

    delete_parser = subparsers.add_parser('delete', help='Delete a command')
    delete_parser.set_defaults(func=delete_command)

    edit_parser = subparsers.add_parser(
        'edit', help='Edit the CSV file')
    edit_parser.set_defaults(func=edit_csv_file)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
