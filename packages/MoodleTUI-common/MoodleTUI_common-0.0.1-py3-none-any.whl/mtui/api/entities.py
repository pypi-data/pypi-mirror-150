from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias
from bs4 import Tag, NavigableString

_BeautifulSoupTag: TypeAlias = Tag | NavigableString


@dataclass()
class Quiz:
    id: int = None
    answered: bool = False
    score: tuple[int, int] = None


@dataclass()
class Lesson:
    id: int = None
    content: list[str] = ...


@dataclass()
class Resource:
    id: int = None
    type: str = ...


@dataclass()
class Assignment:
    id: int = None
    submissionStatus: str = ...
    gradingStatus: str = ...
    content: list[str] = ...


class CourseItem(Enum):
    NULL = None
    QUIZ = Quiz
    LESSON = Lesson
    RESOURCE = Resource
    ASSIGNMENT = Assignment


_CourseContents: TypeAlias = list[Quiz | Lesson | Resource | Assignment]


@dataclass()
class Course:
    id: int = None
    content: _CourseContents = ...
