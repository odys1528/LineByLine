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
        Command.NEXT.parametrized(file_data.filename)
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

    if command is None or command == Command.EXIT:
        return
    else:
        if command == Command.NEXT:
            for file_data in file_datas:
                line = ""
                if condition(file_data.filename, args):
                    line = file_data.next_line()
                else:
                    line = file_data.current_line()
                print_wrapped(line)
        elif command == Command.BACK:
            for file_data in file_datas:
                line = ""
                if condition(file_data.filename, args):
                    line = file_data.back_line()
                else:
                    line = file_data.current_line()
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
    for file_data in file_datas:
        line = file_data.current_line()
        print_wrapped(line)

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

        if answer == Command.EXIT.name:
            exit()

        print_lines(answer, file_datas)
