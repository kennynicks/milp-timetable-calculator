
from typing import List
from config import Days, Lessons, Subjects
from models import BaseEnum, ClassLessonCount, ClassLevel, Clazz, OgsSlot, Teacher

# * Konferenz
CONFERENCE_DAY = Days.Monday
CONFERENCE_LESSON = Lessons.Sixth

# * Lehrer


class Teachers(BaseEnum):
    Ba = Teacher("Ba", [Subjects.Misc, Subjects.Sports], 22)
    Gr = Teacher("Gr", [Subjects.Misc,
                 Subjects.Sports, Subjects.Religion], 27)
    Ka = Teacher("Ka", [Subjects.Misc, Subjects.Sports], 14)
    Ke = Teacher("Ke", [Subjects.Misc,], 22)
    Kl = Teacher("Kl", [Subjects.Misc, Subjects.Sports], 25)
    Ma = Teacher("Ma", [Subjects.Misc, Subjects.Sports], 28)
    Oc = Teacher("Oc", [Subjects.Misc,
                 Subjects.Sports, Subjects.Religion], 23)
    Su = Teacher("Su", [Subjects.Misc, Subjects.Sports,
                 Subjects.Religion, Subjects.Swimming], 16)
    Si = Teacher("Si", [Subjects.Misc, Subjects.Sports], 26)
    Wa = Teacher("Wa", [Subjects.Misc, Subjects.Sports], 18)
    Him = Teacher("Him", [Subjects.Misc, Subjects.Sports,
                  Subjects.English, Subjects.Swimming], 28)

    def length() -> int:
        return len(Teachers)

    def range() -> range:
        return range(Teachers.length())

    @staticmethod
    def by_index(index) -> "BaseEnum":
        return list(Teachers)[index].value

    @staticmethod
    def text_by_index(index) -> str:
        return Teachers.by_index(index).text

# * Klassen


class Classes(BaseEnum):
    FirstA = Clazz("1A", [Teachers.Wa], {
        Subjects.Misc: ClassLessonCount(21, 23)
    })
    FirstB = Clazz("1B", [Teachers.Ka, Teachers.Su], {
        Subjects.Misc: ClassLessonCount(21, 23)
    })
    SecondA = Clazz("2A", [Teachers.Si], {
        Subjects.Misc: ClassLessonCount(22, 24)
    })
    SecondB = Clazz("2B", [Teachers.Ke], {
        Subjects.Misc: ClassLessonCount(22, 24)
    })
    ThirdA = Clazz("3A", [Teachers.Ba], {
        Subjects.Misc: ClassLessonCount(17, 19),
        Subjects.English: ClassLessonCount(3, 3),
        Subjects.Swimming: ClassLessonCount(2, 2),
        Subjects.Religion: ClassLessonCount(1, 1),
        Subjects.Sports: ClassLessonCount(2, 2)
    })
    ThirdB = Clazz("3B", [Teachers.Ma], {
        Subjects.Misc: ClassLessonCount(17, 19),
        Subjects.English: ClassLessonCount(3, 3),
        Subjects.Swimming: ClassLessonCount(2, 2),
        Subjects.Religion: ClassLessonCount(1, 1),
        Subjects.Sports: ClassLessonCount(2, 2)
    })
    FourthA = Clazz("4A", [Teachers.Oc], {
        Subjects.Misc: ClassLessonCount(20, 22),
        Subjects.English: ClassLessonCount(3, 3),
        Subjects.Religion: ClassLessonCount(1, 1),
        Subjects.Sports: ClassLessonCount(2, 2)
    })
    FourthB = Clazz("4B", [Teachers.Gr], {
        Subjects.Misc: ClassLessonCount(20, 22),
        Subjects.English: ClassLessonCount(3, 3),
        Subjects.Religion: ClassLessonCount(1, 1),
        Subjects.Sports: ClassLessonCount(2, 2)
    })
    Remedial = Clazz("Förder", [Teachers.Kl], {
        Subjects.Remedial: ClassLessonCount(10, 10)
    })

    def length() -> int:
        return len(Classes)

    def range() -> range:
        return range(Classes.length())

    @staticmethod
    def but_remedial() -> List["Classes"]:
        return [c for c in Classes if c != Classes.Remedial]

    @staticmethod
    def by_index(index) -> "BaseEnum":
        return list(Classes)[index].value

    @staticmethod
    def text_by_index(index) -> str:
        return Classes.by_index(index).text


# region Förderunterricht Lehrer darf Förder unterrichten
for teacher in Classes.Remedial.value.classteachers:
    teacher.value.subjects.append(Subjects.Remedial)
# endregion


class ClassLevels(BaseEnum):
    First = ClassLevel("erste", [Classes.FirstA, Classes.FirstB])
    Second = ClassLevel("zweite", [Classes.SecondA, Classes.SecondB])
    Third = ClassLevel("dritte", [Classes.ThirdA, Classes.ThirdB])
    Fourth = ClassLevel("vierte", [Classes.FourthA, Classes.FourthB])

    def length() -> int:
        return len(ClassLevels)

    def range() -> range:
        return range(ClassLevels.length())

    @staticmethod
    def by_index(index) -> "BaseEnum":
        return list(ClassLevels)[index].value

    @staticmethod
    def text_by_index(index) -> str:
        return ClassLevels.by_index(index).text


# * Sepzial Stunden für Sport und Schwimmen
SPORT_SLOTS = {
    Days.Wednesday: [Lessons.First, Lessons.Second],
    Days.Friday: [Lessons.First, Lessons.Second]
}

SWIMMING_SLOTS = {
    Days.Tuesday: [Lessons.First, Lessons.Second],
    Days.Thursday: [Lessons.Third, Lessons.Fourth]
}

# region ogs
OGS_DAYS = {
    Days.Tuesday: [Teachers.Oc, Teachers.Kl],
    Days.Wednesday: [Teachers.Si, Teachers.Kl, Teachers.Ma],
    Days.Thursday: [Teachers.Ke, Teachers.Him],
    Days.Friday: [Teachers.Ma, Teachers.Gr],
}
# endregion
