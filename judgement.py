from flask import Flask, render_template, redirect, request, flash, session, url_for
import model

# do we need this? v
app = Flask(__name__)
app.secret_key = "magicbeans"

@app.route("/")
def index():
    user_id = session.get("user_id")
    if user_id:
        return redirect("/users/%s" %user_id)
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    print 5
    user_id = model.authenticate(email, password)
    if user_id != None:
        session['user_id'] = user_id
        return redirect("/users/%s" %user_id)
    else:
        flash("Your login credentials are not recognized. Sorry!")
        return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    r_email = request.form.get("r_email")
    r_password = request.form.get("r_password")
    password_verify = request.form.get("password_verify")
    age = request.form.get("age")
    zip_code = request.form.get("zip_code")

    print 1

    user_email = model.register_check(r_email)
    if user_email == True:
        print 2
        flash("This email is already in use. Please try a new email or login to an existing account.")
        return redirect(url_for ("index"))  
    else:
        if r_password == password_verify:
            print 3
            user_id = model.register_store(r_email, r_password, age, zip_code)
            return redirect("/users/%s" %user_id)
        else:
            print 4
            flash("Your passwords did not match, please try again.")
            return redirect(url_for("index"))



@app.route("/clear")
def clear_session():
    session.clear()
    return redirect(url_for("index"))

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