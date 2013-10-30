from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

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
		return this_user.id
	else:
		return None	

def register_check(email):
	email = db_session.query(User).filter_by(email = email).first()
	if email:
		return True
	else:
		return False

def register_store(email, password, age, zip_code):
	print "Info we are passing to register_store:", email, password, age, zip_code
	new_user = User(email= email, password= password, age=age, zipcode=zip_code)
	db_session.add(new_user)
	db_session.commit()

	db_session.refresh(new_user)
	return new_user.id

	# new_user = db_session.query(User).filter_by(email = email).all()
	#return new_user[0].id

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
