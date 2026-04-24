from flask import Flask, render_template, request, redirect
import json
from datetime import date

app = Flask(__name__)

FILE = "habits.json"

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    data = load_data()
    today = str(date.today())

    for habit in data:
        if today not in data[habit]:
            data[habit][today] = False

    save_data(data)
    return render_template("index.html", habits=data, today=today)

@app.route("/add", methods=["POST"])
def add():
    habit = request.form.get("habit")
    data = load_data()

    if habit not in data:
        data[habit] = {}

    save_data(data)
    return redirect("/")

@app.route("/toggle", methods=["POST"])
def toggle():
    habit = request.form.get("habit")
    today = request.form.get("today")

    data = load_data()
    data[habit][today] = not data[habit].get(today, False)

    save_data(data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
