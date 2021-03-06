from manage_db import ManageDB


class CinemaCLI:

    def __init__(self):
        self.db = ManageDB("cinema_cli.db")

    @staticmethod
    def is_number(string):
        for ch in string:
            if not ch.isdigit():
                return False
        return True

    def input_user_and_tickets(self):
        name = input("Step 1 (User): Choose name> ")

        while True:
            tickets = input("Step 1 (User): Choose number of tickets> ")

            if self.is_number(tickets):
                if int(tickets) > 0:
                    break
            print("Enter a positive integer")

        print("Current movies:")
        self.db.show_movies()
        return (name, int(tickets))

    def choose_movie_id(self):
        while True:
            movie_id = input("Step 2 (Movie): Choose a movie> ")
            if self.is_number(movie_id):
                if self.db.movie_id_exists(int(movie_id)):
                    break
            print("Invalid movie ID: {}".format(movie_id))

        self.db.show_movie_projections(int(movie_id), None)
        return int(movie_id)

    def choose_proj_id(self, movie_id):
        valid_ids = self.db.get_proj_ids_for_movie(movie_id)

        while True:
            proj_id = input("Step 3 (Projection): Choose a projection> ")

            if self.is_number(proj_id):
                if int(proj_id) in valid_ids:
                    break
            print("Invalid projection ID: {}".format(proj_id))

        self.db.print_seats(int(proj_id))
        return int(proj_id)

    def choose_seats(self, seat_count):     # return a list of tuples (row, col)
        seats = []
        for i in range(seat_count):
            seat = i + 1
            pos = input("Step 4 (Seats): Choose seat {}> ".format(seat))
            # check user input
            seats.append(pos)
        return seats

    def print_reservation(self, movie_id, proj_id, seats):
        print("This is your reservation:")
        print("Movie: {}".format(self.db.get_movie_name_by_id(movie_id)))
        print("Date & Time: {}".format(self.db.get_proj_date_and_time(proj_id)))

        seats_msg = "Seats: "
        for i in range(len(seats)):
            if i != len(seats) - 1:
                seats_msg += str(seats[i]) + ", "
            else:
                seats_msg += str(seats[i])
        print(seats_msg)

    def make_reservation(self):
        name, tickets_count = self.input_user_and_tickets()
        movie_id = self.choose_movie_id()
        proj_id = self.choose_proj_id(movie_id)
        seats = self.choose_seats(tickets_count)

        self.print_reservation(movie_id, proj_id, seats)
        # for seat in seats:
        #     self.db.add_reservation(name, proj_id, seat[0], seat[1])

    def main_loop(self):
        while True:
            command = input("> ")

            if command == "show_movies":
                self.db.show_movies()
            elif command.find("show_movie_projections") != -1:
                args = command.strip().split(" ")
                if len(args) == 2:
                    self.db.show_movie_projections(int(args[1]), None)
                elif len(args) == 3:
                    self.db.show_movie_projections(int(args[1]), args[2])
                else:
                    print("Invalid arguments!")
            elif command == "make_reservation":
                self.make_reservation()
            elif command == "help":
                self.print_help()
            elif command == "exit":
                print("Closing Pandora\'s Box!")
                break
            else:
                print("Invalid command!")

    def print_help(self):
        print("show_movies")
        print("show_movie_projections <movie_id> [date]")
        print("make_reservation")
        print("cancel_reservation <name>")
        print("help")
        print("exit")


def main():
    cli = CinemaCLI()
    cli.main_loop()

if __name__ == '__main__':
    main()
