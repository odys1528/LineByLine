import os
import sys
import inquirer
import textwrap
from line_command import Command, FileData


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def generate_choices(file_datas: [FileData]):
    return [
        Command.NEXT.name,
        Command.BACK.name
    ] + [
        Command.NEXT.parametrized(file_data.filename)
        for file_data
        in file_datas
    ] + [
        Command.BACK.parametrized(file_data.filename)
        for file_data
        in file_datas
    ] + [
        Command.EXIT.name
    ]


def print_wrapped(text):
    print(textwrap.fill("> " + text, 100))


def print_lines(raw_command: str, file_datas: [FileData]):
    def condition(name, args) -> bool:
        return True if args == [] else name in args

    (command, args) = Command.decompose(raw_command)

    if command is None:
        return
    elif command == Command.EXIT:
        exit()
    else:
        for file_data in file_datas:
            line = ""
            if condition(file_data.filename, args):
                line = file_data.get_line(command)
            else:
                line = file_data.get_line(Command.CURRENT)
            print_wrapped(line)


if __name__ == "__main__":
    # init
    args = sys.argv[1:]
    if len(args) == 0:
        print("Pass at least 1 path argument")
        exit()

    file_datas = [FileData(path) for path in args]
    choices = generate_choices(file_datas)

    # main loop
    clear()
    print_lines(Command.CURRENT.name, file_datas)

    while True:
        status = [
            inquirer.List(
                'action',
                message="Action?",
                choices=choices,
                carousel=True
            )
        ]
        answer = inquirer.prompt(status)['action']

        clear()

        print_lines(answer, file_datas)
