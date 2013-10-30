from flask import Flask, render_template, redirect, request
import model

# do we need this? v
app = Flask(__name__)

@app.route("/")
def login():
    """
    if user not logged in:
        collect email and password from form
        store in db
    else:
        pass
    """
    pass

@app.route("/", methods=["POST"])
def login():
    """
    if user not logged in:
        collect email and password from form
        store in db
    else:
        pass
    """
    return render_template("index.html")

@app.route("/users")
def list_users():
    user_list = model.db_session.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)

@app.route("/movies")
def list_movies():
    movie_list = model.db_session.query(model.Movies).all()
    return render_template("movie_list.html", movies=movie_list)

@app.route("/users/<user_id>")
def user_profile(user_id):
    return render_template("user_profile.html")

@app.route("/movies/<movie_id>")
def movie_profile(movie_id):
    return render_template("movie_profile.html")

if __name__ == "__main__":
    app.run(debug = True)