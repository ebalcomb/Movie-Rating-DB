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

    user_info = model.authenticate(email, password)
    if user_info != None:
        session['user_id'] = user_info[0]
        session['email'] = user_info[1]
        return redirect("/users/%s" %user_info[0])
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


    user_email = model.register_check(r_email)
    if user_email == True:
        flash("This email is already in use. Please try a new email or login to an existing account.")
        return redirect(url_for ("index"))  
    else:
        if r_password == password_verify:
            user_id = model.register_store(r_email, r_password, age, zip_code)
            return redirect("/users/%s" %user_id)
        else:
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
    user_ratings = model.get_ratings_by_user(user_id)
    return render_template("user_profile.html", viewing_user=user_id, ratings=user_ratings)



@app.route("/movies/<movie_id>")
def movie_profile(movie_id):
    movie_title = model.db_session.query(model.Movies).filter_by(id=movie_id).all()
    movie_ratings = model.get_ratings_by_movie(movie_id)
    return render_template("movie_profile.html", movie_name=movie_title[0].name, movie_id=movie_id, movie_ratings=movie_ratings)

@app.route("/rate_movie/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    best_fit = find_best_fit(movie_id)
    predicted_rating = predict_rating(movie_id, best_fit)

        # take in a new rating from form on page
    user_id = session.get("user_id")
    rating = request.form.get("rating")

    rating_exists = model.rating_check(movie_id, user_id)

    message = respond_to_rating(rating, predicted_rating, rating_exists, user_id, movie_id)
    flash(message)

    return redirect("http://localhost:5000/movies/%s" %movie_id)


def find_best_fit(movie_id):
    u = model.db_session.query(model.User).filter_by(id=session.get("user_id")).first()
    other_ratings = model.db_session.query(model.Ratings).filter_by(movie_id=movie_id).all()
    other_users = []

    for r in other_ratings:
        other_users.append(r.user)
    list_of_pearsons = []
    for other_u in other_users:
        if other_u.id != u.id:
            similarity = u.similarity(other_u)
            sim_tuple = (similarity, other_u)
            list_of_pearsons.append(sim_tuple)
    sorted_pearsons = sorted(list_of_pearsons)
    best_fit = sorted_pearsons[-1]
    
    return best_fit

def predict_rating(movie_id, best_fit):
    best_fit_row = model.db_session.query(model.Ratings).filter_by(user_id=best_fit[1].id, movie_id=movie_id).first()
    best_fit_rating = best_fit_row.rating 
    predict_rating = best_fit_rating*best_fit[0]
    predict_rating_rounded = int(round(predict_rating, 0))

    return predict_rating_rounded


    

def respond_to_rating(rating, predict_rating_rounded, rating_exists, user_id, movie_id):
    if type(rating) == int:
        i_rating = int(rating)
        if i_rating in range(1, 6):

            if rating_exists:
                rating_id = model.rating_update(user_id, movie_id, i_rating)

                if i_rating > predict_rating_rounded:
                    return "Your rating for this movie has been updated. You gave it a %s?!?!? It only deserves a %s!!" %(i_rating, predict_rating_rounded)
                elif i_rating < predict_rating_rounded:
                    return"Your rating for this movie has been updated. You gave it a %s?!?!? It deserves at least a %s!!" %(i_rating, predict_rating_rounded) 

            else:
                rating_id = model.rating_store(user_id, movie_id, i_rating)

                if i_rating > predict_rating_rounded:
                    return"Your rating for this movie has been saved. You gave it a %s?!?!? It only deserves a %s!!" %(i_rating, predict_rating_rounded)
                elif i_rating < predict_rating_rounded:
                    return"Your rating for this movie has been saved. You gave it a %s?!?!? It deserves at least a %s!!" %(i_rating, predict_rating_rounded)

    else:
        return "Your rating must be a number between 1-5"



if __name__ == "__main__":
    app.run(debug = True)