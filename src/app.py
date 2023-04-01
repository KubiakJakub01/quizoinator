from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "mysecret"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/user")
def user():
    if "user" in session:
        user_name = session["user"]
        return render_template("user.html", name=user_name, content=["HTML", "CSS", "JS"])
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        return render_template("login.html")


@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))


if __name__ == "__main__":
    app.run(debug=True)
