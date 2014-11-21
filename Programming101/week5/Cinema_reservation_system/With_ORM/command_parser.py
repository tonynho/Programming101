from cinema import Cinema
import sys


class CommandParser:
    def __init__(self, cinema):
        self.commands = {}  # command : function

    def add_command(self, command, function):
        self.commands[command] = function

    def handle_command(self, command):
        args = command.split(" ")
        print(self.commands[args[0]](*args[1:]))

    def exit(self):
        sys.exit("Closing Pandora\'s Box!")


def main():
    cinema = Cinema()
    command_parser = CommandParser(cinema)

    command_parser.add_command("show_movies", cinema.show_movies)
    command_parser.add_command("show_movie_projections",
                               cinema.show_movie_projections)
    command_parser.add_command("help", cinema.get_help)
    command_parser.add_command("exit", command_parser.exit)

    while True:
        command = input("> ")
        command_parser.handle_command(command)


if __name__ == '__main__':
    main()