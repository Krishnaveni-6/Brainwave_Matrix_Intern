from flask import Flask, render_template, request, redirect, url_for, session
import json
import datetime
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "securekey"  # Secret key for session management
app.permanent_session_lifetime = timedelta(minutes=5)  # Auto logout after 5 min

DATABASE_FILE = "database.json"

# -------------------- Database Functions --------------------
def load_data():
    """Load user data from database.json."""
    with open(DATABASE_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    """Save updated user data to database.json."""
    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file, indent=4)

# -------------------- Home / Login --------------------
@app.route("/", methods=["GET", "POST"])
def login():
    users = load_data()
    if request.method == "POST":
        account = request.form["account"]
        pin = request.form["pin"]

        if account in users:
            user = users[account]

            if user["locked"]:
                return render_template("login.html", error="Account locked due to too many incorrect attempts.")

            if pin == user["pin"]:
                session["account"] = account
                session.permanent = True  # Extend session
                user["attempts"] = 0  # Reset failed attempts
                save_data(users)
                return redirect(url_for("dashboard"))
            else:
                user["attempts"] += 1
                if user["attempts"] >= 3:
                    user["locked"] = True
                    save_data(users)
                    return render_template("login.html", error="Account locked due to too many incorrect attempts.")
                save_data(users)
                return render_template("login.html", error=f"Incorrect PIN. Attempts left: {3 - user['attempts']}")

        return render_template("login.html", error="Invalid account number.")

    return render_template("login.html")

# -------------------- Dashboard --------------------
@app.route("/dashboard")
def dashboard():
    if "account" not in session:
        return redirect(url_for("login"))

    users = load_data()
    account = session["account"]
    user = users[account]

    return render_template("dashboard.html", balance=f"₹{user['balance']:,}", history=user["history"])

# -------------------- Deposit --------------------
@app.route("/deposit", methods=["POST"])
def deposit():
    if "account" not in session:
        return redirect(url_for("login"))

    users = load_data()
    account = session["account"]
    user = users[account]
    amount = int(request.form["amount"])

    if amount > 0:
        user["balance"] += amount
        user["history"].append(f"{datetime.datetime.now()} - Deposited ₹{amount:,}")
        save_data(users)

    return redirect(url_for("dashboard"))

# -------------------- Withdraw --------------------
@app.route("/withdraw", methods=["POST"])
def withdraw():
    if "account" not in session:
        return redirect(url_for("login"))

    users = load_data()
    account = session["account"]
    user = users[account]
    amount = int(request.form["amount"])

    if 0 < amount <= user["balance"]:
        user["balance"] -= amount
        user["history"].append(f"{datetime.datetime.now()} - Withdrawn ₹{amount:,}")
        save_data(users)
    else:
        return render_template("dashboard.html", balance=f"₹{user['balance']:,}", history=user["history"], error="Insufficient balance!")

    return redirect(url_for("dashboard"))

# -------------------- Change PIN --------------------
@app.route("/change_pin", methods=["GET", "POST"])
def change_pin():
    if "account" not in session:
        return redirect(url_for("login"))

    users = load_data()
    account = session["account"]
    user = users[account]

    if request.method == "POST":
        old_pin = request.form["old_pin"]
        new_pin = request.form["new_pin"]
        confirm_pin = request.form["confirm_pin"]

        if old_pin != user["pin"]:
            return render_template("change_pin.html", error="Incorrect old PIN!")

        if len(new_pin) != 4 or not new_pin.isdigit():
            return render_template("change_pin.html", error="New PIN must be 4 digits!")

        if new_pin != confirm_pin:
            return render_template("change_pin.html", error="New PINs do not match!")

        user["pin"] = new_pin
        save_data(users)
        return render_template("change_pin.html", success="PIN successfully changed!")

    return render_template("change_pin.html")

# -------------------- Logout --------------------
@app.route("/logout")
def logout():
    session.pop("account", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
