import os
import requests
import urllib.parse
import json
from flask import redirect, render_template, request, session
from functools import wraps



def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=message), code


def weatherapp(city, cityid):
    api_key = os.environ.get("API_KEY")

    if cityid is None:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}")
    else:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?id={cityid}&units=metric&appid={api_key}")

    return response.json()

def forecast(city):
    api_key = os.environ.get("API_KEY")
    lon = city["lon"]
    lat = city["lat"]
    response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,hourly&appid={api_key}")
    return response.json()



def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
