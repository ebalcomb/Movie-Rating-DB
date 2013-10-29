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

if __name__ == "__main__":
    app.run(debug = True)