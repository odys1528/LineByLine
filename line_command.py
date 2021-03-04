from enum import Enum


class Command(Enum):
    CURRENT = 0
    NEXT = 1
    BACK = -1
    EXIT = 42

    def parametrized(self, filename: str):
        return self.name + " " + filename

    @staticmethod
    def decompose(rawValue: str):
        args = rawValue.split(" ")

        if len(args) == 0:
            args = [rawValue]

        for command in Command:
            if command.name == args[0]:
                return (command, args[1:])
        return (None, args[1:])


class FileData:
    def __init__(self, filename: str):
        self.filename = filename
        self.__current_index = 0
        self.__content = [""]
        self.__read_file()

    def __repr__(self):
        return "<" + self.__class__.__name__ + " " + self.filename + ">"

    def __read_file(self):
        f = open(self.filename, "r")
        self.__content = f.readlines()
        f.close()
        if self.__content == []:
            self.content = [""]

    def get_line(self, command: Command):
        if command == Command.EXIT:
            return None
        else:
            return self.__get_line(command.value)

    def __get_line(self, diff: int):
        index = self.__current_index + diff
        if -len(self.__content) <= index < len(self.__content):
            line = self.__content[index]
            self.__current_index = index
            return line
        else:
            self.__current_index = 0
            return self.__content[self.__current_index]

