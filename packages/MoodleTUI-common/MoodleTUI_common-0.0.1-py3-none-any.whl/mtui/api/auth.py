from requests import Session
from bs4 import BeautifulSoup
from pathurl import Query, URL

from ..types import Namespace
from .entities import _BeautifulSoupTag


def getLoginPage(sess: Session, page: str) -> dict:
    resp = sess.get(page)
    parser = BeautifulSoup(resp.text, "html.parser")

    return {
        "result": parser.find("form", {"id": "login"}),
        "stats": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }


def buildPayload(html: _BeautifulSoupTag, username: str, password: str) -> dict:
    res = {"anchor": "", "username": username, "password": password}

    res.update(
        logintoken=html.find("input", {"type": "hidden", "name": "logintoken"}).get(
            "value"
        )
    )

    return res


def getSesskey(sess: Session, config: Namespace) -> dict:
    url = config.URL.home
    resp = sess.get(url)
    parser = BeautifulSoup(resp.text, "html.parser")

    return {
        "result": parser.find("input", {"id": "sesskey", "type": "hidden"}).get("value"),
        "stats": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }


def login(sess: Session, user: str, passwd: str, config: Namespace):
    url = config.URL.login
    page = getLoginPage(sess, url)
    payload = buildPayload(page.get("result"), user, passwd)
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = sess.post(url, headers=headers, data=payload)

    return {
        "getLoginPage": page.get("stats"),
        "login": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }


def logout(sess: Session, config: Namespace) -> dict:
    url = URL(config.URL.logout)
    sessionKey = getSesskey(sess, config)
    payload = Query().add(sesskey=sessionKey.get("result"))
    url = url.replace(query=payload)

    resp = sess.get(url)
    return {
        "getSesskey": sessionKey.get("stats"),
        "logout": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }
