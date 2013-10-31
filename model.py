from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
import correlation

ENGINE = create_engine("sqlite:///ratings.db", echo=False)
db_session = scoped_session(sessionmaker(bind=ENGINE, 
									autocommit = False,
									autoflush = False))
Base = declarative_base()
Base.query = db_session.query_property()

### Class declarations go here

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable=True)
	password = Column(String(64), nullable=True)
	age = Column(Integer, nullable=True)
	zipcode = Column(String(15), nullable=True)

	def similarity(self, other):
		u_ratings = {}
		paired_ratings = []

		for r in self.ratings:
			u_ratings[ r.movie_id ] = r

		for r in other.ratings:
			u_r = u_ratings.get(r.movie_id)
			if u_r:
				paired_ratings.append( (u_r.rating, r.rating) )

		if paired_ratings:
			return correlation.pearson(paired_ratings)
		else:
			return 0.0



class Movies(Base):
	__tablename__ = "movies"

	id = Column(Integer, primary_key = True)
	name = Column(String(64))
	released_at = Column(Date())
	imdb_url = Column(String(128))

class Ratings(Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key = True)
	movie_id = Column(Integer, ForeignKey('movies.id'))
	user_id = Column(Integer, ForeignKey('users.id'))
	rating = Column(Integer)

	user = relationship("User", backref=backref("ratings", order_by=id))
	movie = relationship("Movies", backref=backref("movies", order_by=id))

# def connect():

### End class declarations

def authenticate(email, password):
	print email
	print password
	this_user = db_session.query(User).filter_by(email = email, password = password).first()
	if this_user:
		return this_user.id, this_user.email
	else:
		return None	

def rating_check(movie_id, user_id):
	rating = db_session.query(Ratings).filter_by(user_id = user_id, movie_id= movie_id).all()
	if rating:
		return True
	else:
		return False


def register_check(email):
	email = db_session.query(User).filter_by(email = email).first()
	if email:
		return True
	else:
		return False

def rating_store(user_id, movie_id, rating):
	new_rating = Ratings(user_id=user_id, movie_id=movie_id, rating=rating)
	db_session.add(new_rating)
	db_session.commit()

	db_session.refresh(new_rating)
	return new_rating.id

def rating_update(user_id, movie_id, rating):
	updated_rating = db_session.query(Ratings).filter_by(user_id=user_id, movie_id=movie_id).first()
	updated_rating.rating = rating
	db_session.commit()
	db_session.refresh(updated_rating)
	print "rating after update:", updated_rating.rating
	return updated_rating






def register_store(email, password, age, zip_code):
	new_user = User(email= email, password= password, age=age, zipcode=zip_code)
	db_session.add(new_user)
	db_session.commit()

	db_session.refresh(new_user)
	return new_user.id

	# new_user = db_session.query(User).filter_by(email = email).all()
	#return new_user[0].id

def get_ratings_by_user(user_id):
	user_ratings = db_session.query(Ratings).filter_by(user_id=user_id)
	return user_ratings


def get_ratings_by_movie(movie_id):
	movie_ratings = db_session.query(Ratings).filter_by(movie_id=movie_id)
	return movie_ratings

def main():
    """In case we need this for something"""

    pass

if __name__ == "__main__":
    main()
