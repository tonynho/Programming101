from movie import Movie
from projection import Projection
from reservation import Reservation

from connection import Base
from connection import engine
from sqlalchemy.orm import Session
import os


class Cinema:
    def __init__(self):
        db_exists = os.path.isfile(os.getcwd() + "/cinema.db")

        Base.metadata.create_all(engine)
        self.session = Session(bind=engine)

        if not db_exists:
            self.__fill_db()

    def add_movie(self, name, rating):
        self.session.add(Movie(name=name, rating=rating))
        self.session.commit()

    def add_projection(self, movie_id, type, date, time):
        self.session.add(
            Projection(movie_id=movie_id, type=type, date=date, time=time))
        self.session.commit()

    def add_reservation(self, user, proj_id, row, col):
        r = Reservation(username=user, projection_id=proj_id, row=row, col=col)
        self.session.add(r)
        self.session.commit()

    def get_reservations_for_name(self, name):
        reservations = self.session.query(Reservation)\
            .filter(Reservation.username == name).all()
        return reservations

    def cancel_reservation(self, reservation):
        username = reservation.username
        self.session.delete(reservation)
        self.session.commit()
        print("Reservation for {} canceled!".format(username))

    def show_movies(self):
        movies = self.session.query(Movie).all()
        return movies

    def show_movie_projections(self, movie_id, date=None):
        if date is None:
            result = self.session.query(Projection).\
                filter(Projection.movie_id == movie_id).all()
        else:
            result = self.session.query(Projection).\
                filter(Projection.movie_id == movie_id,
                       Projection.date == date).all()
        return result

    def __fill_db(self):
        movies = [("The Hunger Games: Catching Fire", 7.9),
                  ("Wreck-It Ralph", 7.8),
                  ("Her", 8.3)]
        projections = [(1, "3D", "2014-04-01", "19:10"),
                       (1, "2D", "2014-04-01", "19:00"),
                       (1, "4DX", "2014-04-02", "21:00"),
                       (3, "2D", "2014-04-05", "20:20"),
                       (2, "3D", "2014-04-02", "22:00"),
                       (2, "2D", "2014-04-02", "19:30")]
        reservations = [("RadoRado", 1, 2, 1), ("RadoRado", 1, 3, 5),
                        ("RadoRado", 1, 7, 8), ("Ivo", 3, 1, 1),
                        ("Ivo", 3, 1, 2), ("Mysterious", 5, 2, 3),
                        ("Mysterious", 5, 2, 4)]

        for movie in movies:
            self.add_movie(*movie)
        for projection in projections:
            self.add_projection(*projection)
        for reservation in reservations:
            self.add_reservation(*reservation)

    def get_help(self):
        help = "show_movies\nshow_movie_projections <movie_id> [date]\n"
        help += "make_reservation <name>\ncancel_reservation <name>\n"
        help += "help\nexit"
        return help

    def print_list(self, list):
        for elem in list:
            print(elem)


def main():
    cinema = Cinema()


if __name__ == '__main__':
    main()
