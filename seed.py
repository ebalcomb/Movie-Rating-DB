import model
import csv
import sys
import datetime

def load_users(session):
    # use u.user
    f = open("seed_data/u.user")
    users = f.readlines()
    for user in users:
        user_col = user.split("|")
        new_user = model.User(id= user_col[0], age=user_col[1], zipcode=user_col[4])
        session.add(new_user)
    session.commit()

def load_movies(session):
    # use u.item
    f = open("seed_data/u.item")
    movies = f.readlines()
    for movie in movies:
        movie_col = movie.split("|")
        title = movie_col[1].split("(")
        title = title[0].strip()
        title = title.decode("latin-1")
        if movie_col[2] != '':
            date = datetime.datetime.strptime(movie_col[2], "%d-%b-%Y")
        else:
            date = datetime.datetime.strptime("01-Jan-2000", "%d-%b-%Y")
        new_movie = model.Movies(id=movie_col[0], name=title, released_at=date, imdb_url=movie_col[3])
        session.add(new_movie)
    session.commit()


def load_ratings(session):
    # use u.data
    f = open("seed_data/u.data")
    ratings = f.readlines()
    for rating in ratings:
        rating_col = rating.split()
        new_rating = model.Ratings(user_id=rating_col[0], movie_id=rating_col[1], rating=rating_col[2])
        session.add(new_rating)
    session.commit()

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    # load_users(session)
    # load_movies(session)
    # load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
