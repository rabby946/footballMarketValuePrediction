from flask import Flask, render_template, redirect, url_for, request, session, flash
import random, math
from datetime import timedelta
import sqlalchemy 
app = Flask(__name__)
app.secret_key = "key"
app.permanent_session_lifetime = timedelta(minutes=10)

#prediction block...

def dist(age, pac, sho, pas, dri, deff, phy, age1, pac1, sho1, pas1, dri1, deff1,   phy1):
    return math.sqrt((age - age1)*(age - age1) * 100 + (pac - pac1)*(pac - pac1) + (sho - sho1)*(sho - sho1) + (pas - pas1)*(pas - pas1) + (dri - dri1)*(dri - dri1) + (deff - deff1)*(deff - deff1) + (phy - phy1)*(phy - phy1))

def do_all(age, pac, sho, pas, dri, deff, phy):
    result = []
    Data = "demoData"
    with open("data.txt", 'r') as f:
        while len(Data) > 0:
            Data = f.readline()
            l = Data.split()
            if len(l) == 0:
                break
            distance = dist(age, pac, sho, pas, dri, deff, phy, int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]), int(l[6]), int(l[7]))
            value = float(l[8])
            result.append((distance, value))
    result.sort()
    newResult = []
    sum = 0
    for i in range(0, len(result)):
        sum += result[i][1]
        newResult.append(sum/(i + 1))
    newResult.sort ()
    print('The lowest market value is : ', newResult[0])
    print('The highest market value is : ', newResult[len(newResult) - 1])
    return (newResult[0] + newResult[1]) / 2

#end prediction

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict", methods = ["GET", "POST"])
def predict():
    val = random.randint(50, 150)
    if request.method == "POST":
        user = request.form["player_name"]
        user = user.title()
        return render_template("player.html", usr=user, vl=val)
    
    return render_template("predict.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user
        if user == "":
            return redirect(url_for("login"))
        flash(f"You are successfully logged in! {user}", "info")
        return redirect(url_for("user", usr=user))
    if "user" in session:
        user = session["user"]
        flash(f"Already logged in! {user}", "info")
        return redirect(url_for("user", usr=session["user"]))
    return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    if "user" in session and session["user"] == usr:
        return render_template("user.html",  usr=usr)
    else:
        flash(f"Your session has been timed out, {usr}...", "info")
        return render_template("base.html")

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been looged out, {user} ......", "info")
    else:
        flash(f" ! You have already logged out !", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__" :
    app.run(debug=True)
