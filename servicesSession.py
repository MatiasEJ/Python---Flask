from flask import g

def set_session_username()-> str:
    username = ""
    if g.username is not "":
        username = g.username
    return username