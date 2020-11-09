import os
import requests
import urllib.parse

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


def weatherapp(city):
    api_key = os.environ.get("API_KEY")
    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    querystring = {"q":city,"lat":"0","lon":"0","callback":"test","id":"2172797","lang":"null","units":"\"metric\""}

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}")

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


