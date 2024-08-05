from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class BaseEnum(Enum):
    @staticmethod
    def length() -> int:
        pass

    @staticmethod
    def range() -> range:
        pass

    @staticmethod
    def by_index(index) -> "BaseEnum":
        pass

    @staticmethod
    def text_by_index(index) -> str:
        pass

    @property
    def index(self) -> int:
        return list(type(self)).index(self)

    @property
    def text(self) -> str:
        return self.value.text


@dataclass
class ClassLessonCount:
    min: int
    max: int


@dataclass
class Subject:
    text: str
    short: str


@dataclass
class Teacher:
    text: str
    subjects: List[Subject]
    lesson_ct: int


@dataclass
class Clazz:
    text: str
    classteachers: List[Teacher]
    lessoncount: Dict[Subject, ClassLessonCount]


@dataclass
class ClassLevel:
    text: str
    classes: List[Clazz]


@dataclass
class Day:
    text: str


@dataclass
class Lesson:
    text: str


@dataclass
class OgsSlot:
    text: str
