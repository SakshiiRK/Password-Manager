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
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

import secrets
import string

# random password generation
def generate_random_password(length=16, use_uppercase=True, use_digits=True, use_symbols=True):
    """
    Generate a random password with the given specifications.
    
    Parameters:
        length (int): Length of the password.
        use_uppercase (bool): Include uppercase letters if True.
        use_digits (bool): Include digits if True.
        use_symbols (bool): Include symbols if True.
    
    Returns:
        str: Generated password.
    """
    if length < 1:
        raise ValueError("Password length must be at least 1")

    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase if use_uppercase else ''
    digits = string.digits if use_digits else ''
    symbols = string.punctuation if use_symbols else ''

    # Combine character sets
    all_characters = lowercase + uppercase + digits + symbols

    if not all_characters:
        raise ValueError("At least one character set must be selected")

    # Generate password
    password = ''.join(secrets.choice(all_characters) for _ in range(length))

    return password

