from flask import Flask, render_template, request
from models import (
    get_active_rentals_count,
    get_available_equipment_count,
    get_latest_rentals
)
app = Flask(__name__)

@app.route("/")
def dashboard():
    aktive_utleier = get_active_rentals_count()
    tilgjengelig_utstyr = get_available_equipment_count()
    siste_utleier = get_latest_rentals()

    return render_template(
        "dashboard.html",
        aktive_utleier=aktive_utleier,
        tilgjengelig_utstyr=tilgjengelig_utstyr,
        siste_utleier=siste_utleier
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/kunder")
def kunder():
    return render_template("kunder.html")

@app.route("/utstyr")
def utstyr():
    return render_template("utstyr.html")

@app.route("/utleie")
def utleie():
    return render_template("utleie.html")

@app.route("/statistikk")
def statistikk():
    return render_template("statistikk.html")


if __name__ == "__main__":
    app.run(debug=True)