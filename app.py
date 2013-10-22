from flask import Flask, render_template, request, redirect, session, url_for, flash
import model
from datetime import datetime

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("username"):
        return "%s is logged in!"%session['username']
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user_id = model.authenticate(username, password)
    if username != None:
        flash("User authenticated!")
        session['user_id'] = user_id
        session['username'] = username
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")
    
    return redirect(url_for("index"))#render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout")
def clear_session():
    session.clear()
    return render_template('index.html')

@app.route("/user/<username>")
def view_user(username):
    user_id = model.get_user_by_name(username)
    wall_posts = model.get_wall_posts_by_id(user_id)
    author_name = model.get_name_by_id(session["user_id"])
    return render_template('wall.html', wall_posts=wall_posts,
                                        username=username,
                                        author_name=author_name)

# owner_id, author_id, created_at, content
@app.route("/user/<username>", methods=["POST"])
def make_new_post(username):
    owner_id = model.get_user_by_name(username)
    author_id = model.get_user_by_name(session["username"])
    created_at = datetime.now()
    content = request.form.get("wall_post")
    model.make_wall_post(owner_id, author_id, created_at, content)
    return redirect(url_for("view_user", username=username))

if __name__ == "__main__":
    app.run(debug = True)
