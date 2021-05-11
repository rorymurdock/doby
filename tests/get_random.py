"""Utilities to help with testing"""
import random
import string


def text(string_length=15):
    """Generate a random string of x length"""

    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))


def number(minimum=0, maximum=9999):
    """Generate a random number"""

    return random.randint(minimum, maximum)


def chars(string_length=8):
    """Generate a random string of letters and digits"""

    return "".join(
        random.choice(string.ascii_uppercase + string.digits)
        for i in range(string_length)
    )
