from requests import Session
from bs4 import BeautifulSoup
from threading import Thread
from itertools import islice
from re import compile

from ..types import Namespace
from .entities import (
    Course,
    CourseItem,
    Assignment,
    Lesson,
    Quiz,
    _BeautifulSoupTag,
    _CourseContents,
)

ID_PARSER = compile("\d{1,}$")


def getCourse(sess: Session, course: Course, config: Namespace) -> dict:
    resp = sess.get(config.Formats.course % course.id)
    scraper = BeautifulSoup(resp.text, "html.parser")

    return {
        "result": iter(scraper.find_all("div", {"class": "activityinstance"})),
        "stats": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }


def get(sess: Session, url: str, output: dict = None):
    output = output or {}
    resp = sess.get(url)

    output = {
        "result": resp.text,
        "stats": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }


def determineType(url: str) -> CourseItem:
    if "quiz" in url:
        return CourseItem.QUIZ
    elif "page" in url:
        return CourseItem.LESSON
    elif "assign" in url:
        return CourseItem.ASSIGNMENT


def parse(sess: Session, course: Course, config: Namespace):
    items = getCourse(sess, course, config)
    res: _CourseContents = []

    for tag in items.get("result"):
        # Type hinting
        tag: _BeautifulSoupTag = tag
        href = tag.find("a").get("href")

        itemID = ID_PARSER.search(href)
        itemID = int(str.join("", islice(itemID.string, *itemID.span())))

        cls = determineType(href).value

        res.append(cls(id=itemID))

    return {
        "result": res,
        "stats": items.get("stats"),
    }


def getCourses(sess: Session, config: Namespace):
    resp = sess.get(config.URL.home)
