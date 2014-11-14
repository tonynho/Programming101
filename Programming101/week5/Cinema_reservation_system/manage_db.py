import sqlite3


class ManageDB:

    def __init__(self, file_name):
        self.connect = sqlite3.connect(file_name)
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()

        self.create_tables()
        self.add_movies()
        self.add_projections()
        self.add_reservations()

    def __del__(self):
        self.connect.close()

    def create_tables(self):
        self.cursor.execute('''PRAGMA foreign_keys = ON;''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS movies(
            id INTEGER PRIMARY KEY, name TEXT, rating REAL);''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS projections(
            id INTEGER PRIMARY KEY, movie_id INTEGER,
            type TEXT, date TEXT, time TEXT,
            FOREIGN KEY(movie_id) REFERENCES movies(id));''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservations(
            id INTEGER PRIMARY KEY, username TEXT, projections_id INTEGER,
            row INTEGER, col INTEGER,
            FOREIGN KEY(projections_id) REFERENCES projections(id));''')

        self.connect.commit()

    def add_movies(self):
        movies = [("The Hunger Games: Catching Fire", 7.9),
                  ("Wreck-It Ralph", 7.8),
                  ("Her", 8.3)]
        self.cursor.executemany('''INSERT INTO movies(name, rating)
            VALUES(?,?);''', movies)
        self.connect.commit()

    def add_projections(self):
        projections = [(1, "3D", "2014-04-01", "19:10"),
                       (1, "2D", "2014-04-01", "19:00"),
                       (1, "4DX", "2014-04-02", "21:00"),
                       (3, "2D", "2014-04-05", "20:20"),
                       (2, "3D", "2014-04-02", "22:00"),
                       (2, "2D", "2014-04-02", "19:30")]
        self.cursor.executemany('''INSERT INTO
            projections(movie_id, type, date, time)
            VALUES(?,?,?,?);''', projections)
        self.connect.commit()

    def add_reservations(self):
        reservations = [("RadoRado", 1, 2, 1), ("RadoRado", 1, 3, 5),
                        ("RadoRado", 1, 7, 8), ("Ivo", 3, 1, 1),
                        ("Ivo", 3, 1, 2), ("Mysterious", 5, 2, 3),
                        ("Mysterious", 5, 2, 4)]
        self.cursor.executemany('''INSERT INTO
            reservations(username, projections_id, row, col)
            VALUES(?,?,?,?);''', reservations)
        self.connect.commit()

    def show_movies(self):
        movies = self.cursor.execute('''SELECT * from movies;''').fetchall()
        output = "[{}] - {} ({})"
        for movie in movies:
            print(output.format(movie['id'], movie['name'], movie['rating']))

    def show_movie_projections(self, movie_id):
        movie = self.cursor.execute('''SELECT name from movies
            WHERE id = ?;''', (movie_id, )).fetchall()
        print("Projections for movie \'{}\':".format(movie[0][0]))
        projections = self.cursor.execute('''SELECT * from projections
            WHERE movie_id = ? ORDER BY date, time;''', (movie_id,)).fetchall()
        output = "[{}] - {} {} ({})"
        for item in projections:
            print(output.format(item['id'], item['date'],
                                item['time'], item['type']))


def main():
    cinema = ManageDB("cinema.db")
    cinema.show_movie_projections(2)


if __name__ == '__main__':
    main()
