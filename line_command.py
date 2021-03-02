from enum import Enum, auto


class Command(Enum):
    NEXT = auto()
    BACK = auto()
    EXIT = auto()

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

    def current_line(self):
        return self.__change_line(0)

    def next_line(self):
        return self.__change_line(1)

    def back_line(self):
        return self.__change_line(-1)

    def __change_line(self, diff: int):
        try:
            line = self.__content[self.__current_index + diff]
            self.__current_index = self.__current_index + diff
            return line
        except IndexError:
            self.__current_index = 0
            return self.__content[self.__current_index]

