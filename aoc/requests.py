import os
import requests


def get_session_cookie() -> str:
    session_cookie = os.getenv("AOC_SESSION")
    if session_cookie is None:
        raise ValueError("AOC_SESSION environment variable is not set")
    return session_cookie


def get_session(session_cookie: str = None) -> requests.Session:
    if session_cookie is None:
        session_cookie = get_session_cookie()
    session = requests.Session()
    session.cookies.set("session", session_cookie)
    return session
