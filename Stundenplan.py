#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pulp import *
from tabulate import tabulate
import itertools

################## INPUT DATA ##################

# Tage
days_cleartext = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
days = range(len(days_cleartext))

# Slots
slots_cleartext = ["1.", "2.", "3.", "4.", "5.", "6."]
slots = range(len(slots_cleartext))

# Klassen
classes_cleartext = ["1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", "Fö"]
classes = range(len(classes_cleartext))

# Fächer
categories_cleartext = ["Sonstiges", "Englisch",
                        "Förder", "Schwimmen", "Religion", "Sport"]
categories = range(len(categories_cleartext))

category_shorttext = ["", " 'E'", " 'FÖ'", " 'Schw'", " 'Rel'", " 'Sp'"]


############################################
Teacher_Ba = 0
Teacher_Gr = 1
Teacher_Kn = 2
Teacher_Ka = 3
Teacher_Ke = 4
Teacher_Kl = 5
Teacher_Ma = 6
Teacher_Oc = 7
Teacher_SB = 8
Teacher_Si = 9
Teacher_Wa = 10
Teacher_Sc = 11
Teacher_Gl = 12
Teacher_Him = 13

Fach_Sonstiges = 0
Fach_Englisch = 1
Fach_Foerder = 2
Fach_Schwimmen = 3
Fach_Religion = 4
Fach_Sport = 5

Tag_Montag = 0
Tag_Dienstag = 1
Tag_Mittwoch = 2
Tag_Donnerstag = 3
Tag_Freitag = 4

Stunde_Erste = 0
Stunde_Zweite = 1
Stunde_Dritte = 2
Stunde_Vierte = 3
Stunde_Fuenfte = 4
Stunde_Sechste = 5
############################################

# Lehrer
teachers_cleartext = [
    "Ba",  # 0
    "Gr",  # 1
    "Kn",  # 2
    "Ka",  # 3
    "Ke",  # 4
    "Kl",  # 5
    "Ma",  # 6
    "Oc",  # 7
    "SB",  # 8
    "Si",  # 9
    "Wa",  # 10
    "Sc",  # 11
    "Gl",  # 12
    "Him"  # 13
]
teachers = range(len(teachers_cleartext))
remedial_teacher = Teacher_Kn
conference_day = Tag_Montag
conference_slot = Stunde_Sechste

#! fächer: sport [alle], schwimmen, englisch, religion [1./2. alle sonst nicht alle]
teacherCategories = [
    [Fach_Sonstiges, Fach_Sport, Fach_Schwimmen, Fach_Englisch],
    [Fach_Sonstiges, Fach_Sport, Fach_Religion],
    [Fach_Sonstiges, Fach_Sport, Fach_Schwimmen],
    [Fach_Sonstiges, Fach_Sport, Fach_Englisch],
    [Fach_Sonstiges, Fach_Sport, Fach_Englisch],
    [Fach_Sonstiges, Fach_Sport],
    [Fach_Sonstiges, Fach_Sport, Fach_Schwimmen],
    [Fach_Sonstiges, Fach_Sport, Fach_Schwimmen, Fach_Religion],
    [Fach_Sonstiges, Fach_Sport, Fach_Englisch],
    [Fach_Sonstiges, Fach_Sport],
    [Fach_Sonstiges, Fach_Sport],
    [Fach_Sonstiges, Fach_Sport, Fach_Englisch],
    [Fach_Sonstiges, Fach_Sport, Fach_Schwimmen],
    [Fach_Sonstiges, Fach_Sport],
]

teacherCategories[remedial_teacher].append(Fach_Foerder)

sport_slots = {
    Tag_Dienstag: [Stunde_Erste, Stunde_Zweite],
    Tag_Mittwoch: [Stunde_Erste, Stunde_Zweite]
}

swim_slots = {
    Tag_Dienstag: [Stunde_Erste, Stunde_Zweite],
    Tag_Donnerstag: [Stunde_Vierte, Stunde_Fuenfte],
    Tag_Freitag: [Stunde_Erste, Stunde_Zweite]
}

class_categories_raw = [
    [22, 2, 0, 0, 0, 0],
    [22, 2, 0, 0, 0, 0],
    [23, 2, 0, 2, 0, 0],
    [23, 2, 0, 2, 0, 0],
    [22, 2, 0, 0, 1, 2],
    [20, 2, 0, 2, 1, 2],
    [22, 2, 0, 0, 1, 2],  # 3
    [22, 2, 0, 0, 1, 2],  # 3
    [0, 0, 10, 0, 0, 0]
]

class_categories = {}
for clazz in classes:
    for category in categories:
        class_categories[(clazz, category)
                         ] = class_categories_raw[clazz][category]

teacherLessons = [
    22, 27, 27, 14,
    19, 26, 24, 24,
    14, 28, 18, 6,
    14, 10
]

classTeachers = {
    0: (Teacher_Si,),
    1: (Teacher_Ke,),
    2: (Teacher_Ba,),
    3: (Teacher_Ma,),
    4: (Teacher_Oc,),
    5: (Teacher_Gr,),
    6: (Teacher_Wa,),
    7: (Teacher_Kl,),
    8: (remedial_teacher,)
}

classTeacherNames = [", ".join(map(lambda x: teachers_cleartext[x],
                                   classTeachers[clazz])) for clazz in classes]

teacherCombinations = list(itertools.combinations(
    teachers, 1)) + list(itertools.combinations(teachers, 2))
teacherCategoryCombinations = []
for combination in teacherCombinations:
    _categories = list(set(itertools.chain.from_iterable(
        [teacherCategories[teacher] for teacher in combination])))
    for category in _categories:
        # * förder nicht in doppelbesetzung
        if category == Fach_Foerder and len(combination) == 2:
            continue
        # * religion nicht in doppelbesetzung
        if category == Fach_Religion and len(combination) == 2:
            continue
        # * schwimmen MUSS in doppelbesetzung
        if category == Fach_Schwimmen and len(combination) == 1:
            continue
        # * sport KEINE doppelbesetzung
        if category == Fach_Sport and len(combination) == 2:
            continue
        # * Him nur in Doppelbesetzung
        if Teacher_Him in combination and len(combination) == 1:
            continue
        # * Gl nur in Doppelbesetzung
        if Teacher_Gl in combination and len(combination) == 1:
            continue
        # * Kl macht keinen Sport
        if Teacher_Kl in combination and category == Fach_Sport:
            continue
        # * Kl macht kein Schwimmen
        if Teacher_Kl in combination and category == Fach_Schwimmen:
            continue
        # * Sc macht nur Englisch oder Doppelbesetzung:
        if Teacher_Sc in combination and category != Fach_Englisch and len(combination) == 2:
            continue
        teacherCategoryCombinations.append({
            "teachers": combination,
            "category": category
        })
lessons = range(len(teacherCategoryCombinations))

categoryLessons = {}

for category in categories:
    _lessons = []
    for lesson in lessons:
        if teacherCategoryCombinations[lesson]["category"] == category:
            _lessons.append(lesson)
    categoryLessons[category] = _lessons

teacherToLessons = {}
for teacher in teachers:
    _lessons = []
    for lesson in lessons:
        if teacher in teacherCategoryCombinations[lesson]["teachers"]:
            _lessons.append(lesson)
    teacherToLessons[teacher] = _lessons

slot_combinations = {
    0: [0, 0, 0, 0, 0, 0],
    1: [1, 0, 0, 0, 0, 0],
    2: [0, 1, 0, 0, 0, 0],
    3: [0, 0, 1, 0, 0, 0],
    4: [0, 0, 0, 1, 0, 0],
    5: [0, 0, 0, 0, 1, 0],
    6: [0, 0, 0, 0, 0, 1],
    7: [1, 1, 0, 0, 0, 0],
    8: [0, 1, 1, 0, 0, 0],
    9: [0, 0, 1, 1, 0, 0],
    10: [0, 0, 0, 1, 1, 0],
    11: [0, 0, 0, 0, 1, 1],
    12: [1, 1, 1, 0, 0, 0],
    13: [0, 1, 1, 1, 0, 0],
    14: [0, 0, 1, 1, 1, 0],
    15: [0, 0, 0, 1, 1, 1],
    16: [1, 1, 1, 1, 0, 0],
    17: [0, 1, 1, 1, 1, 0],
    18: [0, 0, 1, 1, 1, 1],
    19: [1, 1, 1, 1, 1, 0],
    20: [0, 1, 1, 1, 1, 1],
    21: [1, 1, 1, 1, 1, 1],
}

combinationToStartSlot = {
    0: -1,
    1: Stunde_Erste,
    2: Stunde_Zweite,
    3: Stunde_Dritte,
    4: Stunde_Vierte,
    5: Stunde_Fuenfte,
    6: Stunde_Sechste,
    7: Stunde_Erste,
    8: Stunde_Zweite,
    9: Stunde_Dritte,
    10: Stunde_Vierte,
    11: Stunde_Fuenfte,
    12: Stunde_Erste,
    13: Stunde_Zweite,
    14: Stunde_Dritte,
    15: Stunde_Vierte,
    16: Stunde_Erste,
    17: Stunde_Zweite,
    18: Stunde_Dritte,
    19: Stunde_Erste,
    20: Stunde_Zweite,
    21: Stunde_Erste
}

last_slot_to_slot_combinations = {
    -1: (0,),
    0: (1,),
    1: (2, 7,),
    2: (3, 8, 12,),
    3: (4, 9, 13, 16,),
    4: (5, 10, 14, 17, 19,),
    5: (6, 11, 15, 18, 20, 21,),
}


school_end_slots = [-1, *slots]


n_slot_combinations = range(len(slot_combinations))

grade_levels = {
    0: (0, 1,),
    1: (2, 3,),
    2: (4, 5,),
    3: (6, 7,)
}

grade_levels_clear_text = {
    0: "erste",
    1: "zweite",
    2: "dritte",
    3: "vierte"
}

n_grade_levels = range(len(grade_levels))

ogs_teachers = [
    Teacher_Gl,
    Teacher_Kn,
    Teacher_Ma
]
################################################

##################  VARIABLES  ##########################
p_school_end_deviation = {
    (day, grade_level): LpVariable("Stundenabweichung der Stufe %s am %s" %
                                   (grade_levels_clear_text[grade_level], days_cleartext[day]), cat=LpInteger, lowBound=0)
    for grade_level in n_grade_levels
    for day in days
}

p_no_school_conference_day = LpVariable(
    "Keine Schule am Konferenz-Tag", cat=LpInteger, lowBound=0, upBound=len(teachers))
p_two_hours_on_conference_day = {
    (teacher): LpVariable(
        "Zwei Stunden Schule am Konferenz-Tag von Lehrer %s"
        % (teacher), cat=LpInteger, lowBound=0, upBound=len(slots))
    for teacher in teachers
}


class_teached_by = {
    (clazz, teacher): LpVariable("Klasse %s wird in der Woche von %s unterrichtet"
                                 % (classes_cleartext[clazz],
                                    teachers_cleartext[teacher],
                                    ), cat=LpBinary)
    for clazz in classes
    for teacher in teachers
}

teacher_day_slot_combination = {
    (teacher, day, slot_combination): LpVariable("Am Tag %s hat Lehrer %s die Stunden-Kombination %s"
                                                 % (days_cleartext[day],
                                                    teachers_cleartext[teacher],
                                                    slot_combination,
                                                    ), cat=LpBinary)
    for day in days
    for teacher in teachers
    for slot_combination in n_slot_combinations
}

x = {
    (day, slot, clazz, lesson): LpVariable("Am %s in der %s Stunde wird in der Klasse %s %s von %s unterrichtet"
                                           % (days_cleartext[day],
                                              slots_cleartext[slot],
                                              classes_cleartext[clazz],
                                              teacherCategoryCombinations[lesson]["category"],
                                              teacherCategoryCombinations[lesson]["teachers"]
                                              ), cat=LpBinary)
    for day in days
    for slot in slots
    for clazz in classes
    for lesson in lessons
}

slot_used = {
    (day, slot, clazz): LpVariable("Am Tag %s in der Klasse %s wird in der %s Stunde unterrichtet"
                                   % (days_cleartext[day],
                                      classes_cleartext[clazz],
                                      slots_cleartext[slot],
                                      ), cat=LpBinary)
    for day in days
    for slot in slots
    for clazz in classes
}

teacher_school_end = {
    (teacher, day, school_end_slot): LpVariable("Am %s hat %s ab Slot %s frei"
                                                % (days_cleartext[day], teachers_cleartext[teacher], school_end_slot), cat=LpBinary)
    for day in days
    for teacher in teachers
    for school_end_slot in school_end_slots
}

same_day_school_end = {
    (day, school_end_slot): LpVariable("Am %s haben alle ab der %s Stunde schluss" % (days_cleartext[day], school_end_slot), cat=LpBinary,)
    for day in days
    for school_end_slot in school_end_slots
}

teacher_day_ogs = {
    (teacher, day): LpVariable("%s hat am %s OGS" % (teachers_cleartext[teacher], days_cleartext[day]), cat=LpBinary)
    for teacher in teachers
    for day in days
}

#########################################################

problem = LpProblem("Stundenplan", sense=LpMaximize)

# **************************************************** PERSONAL CONSTRAINTS
# * Ba unterrichtet nur die eigene Klasse in Englisch
problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                      for day in days
                            for slot in slots
                            for clazz in classes
                            for lesson in lessons
                            if Teacher_Ba not in classTeachers[clazz]
                            and teacherCategoryCombinations[lesson]["category"] == Fach_Englisch
                            and Teacher_Ba in teacherCategoryCombinations[lesson]["teachers"]) == 0)

# * Ba startet um 8 oder hat frei
for day in days:
    problem.addConstraint(lpSum(x[(day, 0, clazz, lesson)]
                                for clazz in classes
                                for lesson in teacherToLessons[Teacher_Ba]) +
                          teacher_school_end[(Teacher_Ba, day, -1)] == 1)


# * Ba hat Sport in der eigenen Klasse
problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                      for day in days
                            for slot in slots
                            for clazz in classes
                            for lesson in lessons
                            if Teacher_Ba not in classTeachers[clazz]
                            and teacherCategoryCombinations[lesson]["category"] == Fach_Sport
                            and Teacher_Ba in teacherCategoryCombinations[lesson]["teachers"]) == 0)

# * Ba hat Schwimmen in der eigenen Klasse
problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                      for day in days
                            for slot in slots
                            for clazz in classes
                            for lesson in lessons
                            if Teacher_Ba not in classTeachers[clazz]
                            and teacherCategoryCombinations[lesson]["category"] == Fach_Schwimmen
                            and Teacher_Ba in teacherCategoryCombinations[lesson]["teachers"]) == 0)

# * Ke unterrichtet nur die eigene Klasse in Englisch
problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                      for day in days
                            for slot in slots
                            for clazz in classes
                            for lesson in lessons
                            if Teacher_Ke not in classTeachers[clazz]
                            and teacherCategoryCombinations[lesson]["category"] == Fach_Englisch
                            and Teacher_Ke in teacherCategoryCombinations[lesson]["teachers"]) == 0)

# * Sc unterrichtet nur 4. Klassen in Englisch
problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                            for day in days
                            for slot in slots
                            for lesson in lessons
                            for clazz in classes[6:-1]
                            if teacherCategoryCombinations[lesson]["category"] == Fach_Englisch
                            and Teacher_Sc in teacherCategoryCombinations[lesson]["teachers"]) == 0)

# * Gl nur dienstags volltags da
for day in [Tag_Montag, Tag_Mittwoch, Tag_Donnerstag, Tag_Freitag]:
    problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)] for slot in slots[0:2]
                          for clazz in classes
                                for lesson in teacherToLessons[Teacher_Gl]) == 0)

# * Ma startet um 8 oder hat frei
for day in days:
    problem.addConstraint(lpSum(x[(day, 0, clazz, lesson)]
                                for clazz in classes
                                for lesson in teacherToLessons[Teacher_Ma]) +
                          teacher_school_end[(Teacher_Ma, day, -1)] == 1)


# * Ma hat Sport in der eigenen Klasse
problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                      for day in days
                            for slot in slots
                            for clazz in classes
                            for lesson in lessons
                            if Teacher_Ma not in classTeachers[clazz]
                            and teacherCategoryCombinations[lesson]["category"] == Fach_Sport
                            and Teacher_Ma in teacherCategoryCombinations[lesson]["teachers"]) == 0)

# * Ma hat Schwimmen in der eigenen Klasse
problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                      for day in days
                            for slot in slots
                            for clazz in classes
                            for lesson in lessons
                            if Teacher_Ma not in classTeachers[clazz]
                            and teacherCategoryCombinations[lesson]["category"] == Fach_Schwimmen
                            and Teacher_Ma in teacherCategoryCombinations[lesson]["teachers"]) == 0)

# * Wa startet um 8 oder hat frei
for day in days:
    problem.addConstraint(lpSum(x[(day, 0, clazz, lesson)]
                                for clazz in classes
                                for lesson in teacherToLessons[Teacher_Wa]) +
                          teacher_school_end[(Teacher_Wa, day, -1)] == 1)

# * Wa hat an einem Tag frei
p_wa_no_school_once = LpVariable(
    "Wa hat jeden Tag Schule", cat=LpBinary)

problem.addConstraint(
    lpSum(teacher_school_end[(Teacher_Wa, day, -1)] for day in days) >= p_wa_no_school_once)

# * Sb unterrichtet nur in der 1. bis 3. Stufe Englisch
problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                            for day in days
                            for slot in slots
                            for lesson in lessons
                            for clazz in classes[6:-1]
                            if teacherCategoryCombinations[lesson]["category"] == Fach_Englisch
                            and Teacher_Sc in teacherCategoryCombinations[lesson]["teachers"]) == 0)

# * Ka startet um 9 oder hat frei
for day in days:
    problem.addConstraint(lpSum(teacher_day_slot_combination[(Teacher_Ka, day, combination)]
                                for combination in n_slot_combinations
                                if combinationToStartSlot[combination] == Stunde_Zweite or combinationToStartSlot[combination] == -1) == 1)
# * Ka kann 3 Tage nur bis 12:45 (Tage nicht festgesetzt)
problem.addConstraint(lpSum(
    x[(day, Stunde_Sechste, clazz, lesson)] for day in days for clazz in classes for lesson in teacherToLessons[Teacher_Ka]) <= 2)

# ****************************************************


##################  CONSTRAINTS  ########################
# * Jede Klasse hat genau n stunden aus kategorie c pro Woche
for clazz in classes:
    for category in categories:
        problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                    for day in days
                                    for slot in slots
                                    for lesson in categoryLessons[category]
                                    ) == class_categories[clazz, category])

for clazz in classes:
    for lesson in lessons:
        if class_categories[clazz, teacherCategoryCombinations[lesson]["category"]] == 0:
            for day in days:
                for slot in slots:
                    problem.addConstraint(x[(day, slot, clazz, lesson)] == 0)

# * Jede klasse hat im slot 0 jeden tages unterricht
for day in days:
    for clazz in classes[:-1]:
        problem.addConstraint(
            lpSum(x[(day, Stunde_Erste, clazz, lesson)] for lesson in lessons) == 1)

# * Jeder Lehrer darf an jedem Tag in jedem Slot nur eine Klasse unterrichten
for teacher in teachers:
    for day in days:
        for slot in slots:
            problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                        for clazz in classes
                                        for lesson in lessons
                                        if teacher in teacherCategoryCombinations[lesson]["teachers"]
                                        ) == lpSum(
                teacher_day_slot_combination[(teacher, day, combination)] * slot_combinations[combination][slot] for
                combination in n_slot_combinations))

# * An jedem Tag hat jede Klasse maximal eine Stunde englisch
for day in days:
    for clazz in classes[:-1]:
        problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                              for slot in slots for lesson in categoryLessons[Fach_Englisch]) <= 1)

# * An jedem Tag hat jede Klasse maximal eine Stunde religion
for day in days:
    for clazz in classes[:-1]:
        problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                              for slot in slots for lesson in categoryLessons[Fach_Religion]) <= 1)

# * Für jeden Slot darf nur eine Combination ausgewählt sein
for day in days:
    for slot in slots:
        for clazz in classes:
            problem.addConstraint(
                lpSum(x[(day, slot, clazz, lesson)] for lesson in lessons) == 1 * slot_used[(day, slot, clazz)])

# * Jeder Lehrer darf nur eine bestimmte Stundenzahl pro Woche unterrichten
for teacher in teachers:
    problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                for day in days
                                for slot in slots
                                for clazz in classes
                                for lesson in lessons
                                if teacher in teacherCategoryCombinations[lesson]["teachers"]
                                )
                          + lpSum(teacher_day_ogs[(teacher, day)]
                                  for day in days)
                          == teacherLessons[teacher])

# * Alle Klassenstufen haben paarweise gleichzeitig schluss (1a+1b gleichzeitig!) => kann muss aber nicht
for grade_level in n_grade_levels:
    for day in days:
        for clazz in grade_levels[grade_level][:-1]:
            problem.addConstraint((lpSum(x[(day, slot, clazz, lesson)]
                                         for lesson in lessons
                                         for slot in slots)-lpSum(
                x[(day, slot, clazz+1, lesson)]
                for lesson in lessons
                for slot in slots)) == p_school_end_deviation[(day, grade_level)])

# * Keine FREISTUNDEN
for day in days:
    for clazz in classes[:-1]:
        for slot in slots[:-1]:
            problem.addConstraint(
                slot_used[(day, slot, clazz)] - slot_used[(day, slot + 1, clazz)] >= 0)

# * Alle Lehrer haben mindestens einmal die Woche gleichzeitig Schluss => muss (am besten Montags)
for teacher in teachers:
    for day in days:
        for school_end_slot in school_end_slots:
            problem.addConstraint(teacher_school_end[(
                teacher, day, school_end_slot)] ==
                lpSum(teacher_day_slot_combination[(teacher, day, slot_combination)] for slot_combination in last_slot_to_slot_combinations[school_end_slot]))

for day in days:
    for school_end_slot in school_end_slots:
        problem.addConstraint((lpSum(teacher_school_end[(teacher, day, school_end_slot)] for teacher in teachers) - (len(
            teachers)-lpSum(teacher_school_end[(teacher, day, -1)]for teacher in teachers)))*-1 <= 13*(1-same_day_school_end[(day, school_end_slot)]))

for day in days:
    problem.addConstraint(lpSum(same_day_school_end[(
        day, school_end_slot)] for school_end_slot in school_end_slots) <= 1)


# * am Konferenztag hat niemand frei
problem.addConstraint(lpSum(teacher_school_end[(
    teacher, conference_day, -1)] for teacher in teachers) == p_no_school_conference_day)

# * Alle Klassen haben nach der 5. Stunde Schluss am Konferenztag
problem.addConstraint(same_day_school_end[(
    conference_day, conference_slot-1)] == 1)

# * Freitags 5 Stunden
problem.addConstraint(same_day_school_end[(Tag_Freitag, Stunde_Fuenfte)] == 1)

# * am konferenztag haben möglichst alle die letzten beiden Stunden unterricht
for teacher in teachers:
    problem.addConstraint(lpSum(x[(conference_day, slot, clazz, lesson)]
                                for clazz in classes
                                for slot in slots
                                for lesson in lessons
                                if teacher in teacherCategoryCombinations[lesson]["teachers"]
                                ) == p_two_hours_on_conference_day[(teacher)])

# * keine SPRINGSTUNDEN
# nicht zwingend aber höchst wünschenswert
for teacher in teachers:
    for day in days:
        problem.addConstraint(lpSum(teacher_day_slot_combination[(
            teacher, day, slot_combination)] for slot_combination in n_slot_combinations) == 1)

# * Minimum 4h / Tag
for day in days:
    for clazz in classes[:-1]:
        problem.addConstraint(
            lpSum(slot_used[(day, slot, clazz)] for slot in slots) >= 4)

for day in days:
    for clazz in classes[:-1]:
        for slot in slots[:4]:
            problem.addConstraint(slot_used[(day, slot, clazz)] == 1)

for clazz in classes:
    for teacher in teachers:
        problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                    for day in days
                                    for slot in slots
                                    for lesson in lessons
                                    if teacher in teacherCategoryCombinations[lesson]["teachers"]
                                    ) <= 29 * class_teached_by[(clazz, teacher)])

# nicht zwingend aber höchst wünschenswert (möglichst nicht 1./2.)
# # * Jede Klasse hat maximal drei Lehrkräfte (frisst unnormal viel Zeit)
for clazz in classes:
    for teacher in classTeachers[clazz]:
        problem.addConstraint(class_teached_by[(clazz, teacher)] == 1)

teacherCategoryCount = {}
for category in categories:
    teacherCategoryCount[category] = [0, []]
    for teacher in teachers:
        if category in teacherCategories[teacher]:
            teacherCategoryCount[category][0] += 1
            teacherCategoryCount[category][1].append(teacher)

for category in categories:
    for clazz in classes:
        if class_categories[clazz, category] > 0 and teacherCategoryCount[category][0] == 1:
            problem.addConstraint(
                class_teached_by[(clazz, teacherCategoryCount[category][1][0])] == 1)


for clazz in classes:
    problem.addConstraint(
        lpSum(class_teached_by[(clazz, teacher)] for teacher in teachers) <= 3)


# * Die Klassenleitung hat mindestens 2 Stunden pro Tag in seiner Klasse
for clazz in classes:
    for day in days:
        problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                    for lesson in lessons
                                    for slot in slots
                                    for teacher in teacherCategoryCombinations[lesson]["teachers"]
                                    if teacher in classTeachers[clazz]) >= 2)

# * OGS => 3 Lehrer opfern jeweils eine Stunde die Woche für OGS (anschluss an die 6. Stunde 14-15uhr) keine springstunde
# genau drei mal ogs
problem.addConstraint(lpSum(
    teacher_day_ogs[(teacher, day)] for teacher in teachers for day in days) == 3)

# vordefinierte ogs teachers
for ogs_teacher in ogs_teachers:
    problem.addConstraint(
        lpSum(teacher_day_ogs[(ogs_teacher, day)] for day in days) == 1)

# jeder lehrer maximal einmal ogs
for teacher in teachers:
    problem.addConstraint(
        lpSum(teacher_day_ogs[(teacher, day)] for day in days) <= 1)

# an jedem tag maxinmal einmal ogs
for day in days:
    problem.addConstraint(
        lpSum(teacher_day_ogs[(teacher, day)] for teacher in teachers) <= 1)

problem.addConstraint(lpSum(teacher_day_ogs[(
    teacher, conference_day)] for teacher in teachers) == 0)  # *am konferenz tag keine ogs

# im anschluss an die sechste stunde
for teacher in teachers:
    for day in days:
        problem.addConstraint(
            teacher_day_ogs[(teacher, day)] <= teacher_school_end[(teacher, day, Stunde_Sechste)])

# * förder: 2 stunden 4-5 mal die woche migrationskinder; möglichst alle klassen unterricht (muss aber nicht); Ein Lehrer
for day in days:
    # zwei stunden am tag förderunterricht
    problem.addConstraint(
        lpSum(slot_used[(day, slot, 8)] for slot in slots) == 2)
    # förderunterricht nur in der 1.-4. Stunde
    problem.addConstraint(lpSum(slot_used[(day, Stunde_Fuenfte, 8)]) == 0)
    # förderunterricht nur in der 1.-4. Stunde
    problem.addConstraint(lpSum(slot_used[(day, Stunde_Sechste, 8)]) == 0)

# * religion in der letzten stunde
# 3. und 4. Stufe
for day in days:
    for clazz in classes[4:-1]:
        for slot in slots[:-1]:
            problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)] for lesson in categoryLessons[Fach_Religion]) <= 1 -
                                  slot_used[(day, slot+1, clazz)])

# * teils fixe sportzeiten (mehrere Klassen gleichzeitig => zwei hallen 3./4.)
# stufenweise zusammen
# ein lehrer
# doppelstunde

for clazz in classes[:-1]:
    if class_categories_raw[clazz][Fach_Sport] == 0:
        continue
    for day in days:
        for slot in slots:
            if day in sport_slots and slot in sport_slots[day]:
                continue
            for lesson in categoryLessons[Fach_Sport]:
                problem.addConstraint(x[(day, slot, clazz, lesson)] == 0)

for sport_day in sport_slots:
    for sport_slot in sport_slots[sport_day]:
        problem.addConstraint(lpSum(x[(sport_day, sport_slot, clazz, lesson)]  # 2 klassen gleichzeitig sport
                              for clazz in classes[:-1]
                              for lesson in categoryLessons[Fach_Sport]) == 2)
        problem.addConstraint(lpSum(x[(sport_day, sport_slot, 4, lesson)]  # dritte stufe hat gleichzeitig sport
                                    for lesson in categoryLessons[Fach_Sport]) == lpSum(
            x[(sport_day, sport_slot, 5, lesson)]
            for lesson in categoryLessons[Fach_Sport]))
        problem.addConstraint(lpSum(x[(sport_day, sport_slot, 6, lesson)]  # vierte stufe hat gleichzeitig sport
                                    for lesson in categoryLessons[Fach_Sport]) == lpSum(
            x[(sport_day, sport_slot, 7, lesson)]
            for lesson in categoryLessons[Fach_Sport]))
    # gleicher lehrer in doppelstunde
    for lesson in categoryLessons[Fach_Sport]:
        for clazz in classes[4:-1]:
            problem.addConstraint(x[(sport_day, sport_slots[sport_day][0], clazz, lesson)] == x[(
                sport_day, sport_slots[sport_day][1], clazz, lesson)])

# * fixe schwimmzeiten muss Doppelstunde sein (selber lehrer)
for swim_day in swim_slots:
    for swim_slot in swim_slots[swim_day]:
        problem.addConstraint(lpSum(x[(swim_day, swim_slot, clazz, lesson)]  # 2 klassen gleichzeitig schwimmen
                              for clazz in classes[:-1]
                              for lesson in categoryLessons[Fach_Schwimmen]) == 1)

for clazz in classes[:-1]:
    if class_categories_raw[clazz][Fach_Schwimmen] == 0:
        continue
    for day in days:
        for slot in slots:
            if day in swim_slots and slot in swim_slots[day]:
                continue
            for lesson in categoryLessons[Fach_Schwimmen]:
                problem.addConstraint(x[(day, slot, clazz, lesson)] == 0)

for swim_day in swim_slots:
    # gleicher lehrer in doppelstunde
    for lesson in categoryLessons[Fach_Schwimmen]:
        for clazz in classes[:-1]:
            if class_categories_raw[clazz][Fach_Schwimmen] == 0:
                continue
            problem.addConstraint(x[(swim_day, swim_slots[swim_day][0], clazz, lesson)] == x[(
                swim_day, swim_slots[swim_day][1], clazz, lesson)])

# * Stufen haben gleich viele Doppelbesetzungen
for clazz in [0, 2, 4, 6]:
    problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                for day in days
                                for slot in slots
                                for lesson in lessons
                                if len(teacherCategoryCombinations[lesson]["teachers"]) == 2 and teacherCategoryCombinations[lesson]["category"] != Fach_Schwimmen) ==
                          lpSum(x[(day, slot, clazz+1, lesson)]
                                for day in days
                                for slot in slots
                                for lesson in lessons
                                if len(teacherCategoryCombinations[lesson]["teachers"]) == 2 and teacherCategoryCombinations[lesson]["category"] != Fach_Schwimmen))

# * Dritte Klassen haben mindestens drei Stunden in Doppelbesetzung
for clazz in [4, 5]:
    problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                for day in days
                                for slot in slots
                                for lesson in lessons
                                if len(teacherCategoryCombinations[lesson]["teachers"]) == 2 and teacherCategoryCombinations[lesson]["category"] != Fach_Schwimmen) >= 3)

# * Vierte Klassen haben mindestens drei Stunden in Doppelbesetzung
for clazz in [6, 7]:
    problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                for day in days
                                for slot in slots
                                for lesson in lessons
                                if len(teacherCategoryCombinations[lesson]["teachers"]) == 2 and teacherCategoryCombinations[lesson]["category"] != Fach_Schwimmen) >= 2)

########################################################


#################  OBJECTIVE  ##################
# Maximize teacher hours in main class
problem.setObjective(
    lpSum(x[(day, slot, clazz, lesson)]
          for day in days
          for slot in slots
          for clazz in classes
          for lesson in lessons
          for teacher in teacherCategoryCombinations[lesson]["teachers"]
          if teacher in classTeachers[clazz]
          ) - lpSum(p_school_end_deviation[(day, grade_level)]
                    for grade_level in n_grade_levels
                    for day in days)
    - p_no_school_conference_day
    + p_wa_no_school_once*30
    + lpSum(p_two_hours_on_conference_day[(teacher)]
            for teacher in teachers)
    + lpSum(x[(day, slot, clazz, lesson)]  # * gewichtung doppelbesetzungen => vorallem 1./2.
            for day in days
            for slot in slots
            for clazz in range(4)
            for lesson in lessons
            if len(teacherCategoryCombinations[lesson]["teachers"]) == 2
            ) * 100
    + lpSum(x[(day, slot, clazz, lesson)]  # * gewichtung doppelbesetzungen => vorallem 1./2.
            for day in days
            for slot in slots
            for clazz in range(4, 8)
            for lesson in lessons
            if len(teacherCategoryCombinations[lesson]["teachers"]) == 2
            ) * 1
    + lpSum(x[(day, slot, clazz, lesson)]  # * GL macht sport und schwimmen
            for day in days
            for slot in slots
            for clazz in classes[:-1]
            for lesson in lessons
            if Teacher_Gl in teacherCategoryCombinations[lesson]["teachers"]
            and (teacherCategoryCombinations[lesson]["category"] == Fach_Sport or teacherCategoryCombinations[lesson]["category"] == Fach_Schwimmen)*50
            )
    + lpSum(x[(day, slot, clazz, lesson)]  # * Ka macht gerne Englisch in der 1.
            for day in days
            for slot in slots
            for clazz in classes[:2]
            for lesson in teacherToLessons[Teacher_Ka]
            if teacherCategoryCombinations[lesson]["category"] == Fach_Englisch)*50
    + lpSum(x[(day, slot, clazz, lesson)]  # * Gr macht gerne Religion in der 1.
            for day in days
            for slot in slots
            for clazz in classes[6:-1]
            for lesson in teacherToLessons[Teacher_Gr]
            if teacherCategoryCombinations[lesson]["category"] == Fach_Religion)*50
)
################################################
# The problem is solved using PuLP's choice of Solver
print("Constraints: %s" % (len(problem.constraints)))
problem.solve(GUROBI_CMD())

#################  OUTPUT  ##################

# The status of the solution is printed to the screen
print("Status:", LpStatus[problem.status])
if problem.status == LpStatusNotSolved:
    exit()

day_data = {}
for day in days:
    day_data[day] = []

for day in days:
    for slot in slots:
        slot_data = [slots_cleartext[slot]]
        day_data[day].append(slot_data)
        for clazz in classes:
            if sum(value(x[(day, slot, clazz, lesson)]) for lesson in lessons) == 0:
                slot_data.append("-")
                continue

            for lesson in lessons:
                if value(x[(day, slot, clazz, lesson)]) == 0:
                    continue
                slot_data.append(", ".join(list(map(
                    lambda x: teachers_cleartext[x], teacherCategoryCombinations[lesson]["teachers"]))) + category_shorttext[
                    teacherCategoryCombinations[lesson]["category"]])
    day_data[day].append(["7."])
    teacher_ogs_data = ["8."]
    for teacher in teachers:
        if value(teacher_day_ogs[(teacher, day)]) == 1:
            teacher_ogs_data.append("OGS von %s" %
                                    (teachers_cleartext[teacher]))
    day_data[day].append(teacher_ogs_data)

for day in days:
    print()
    print(days_cleartext[day] + ":")
    print(tabulate(day_data[day], headers=[
        "Stunde", *["%s - %s" % x for x in zip(classes_cleartext, classTeacherNames)]]))


category_clazz_data = []

for category in categories:
    _categories = [categories_cleartext[category]]
    for clazz in classes:
        hours = sum(value(x[(day, slot, clazz, lesson)])
                    for day in days for slot in slots for lesson in lessons if teacherCategoryCombinations[lesson]["category"] == category)
        _categories.append("%d" %
                           (hours))
    category_clazz_data.append(_categories)

print()
print(tabulate(category_clazz_data, headers=["Fach", *classes_cleartext]))


print()
for day in days:
    if sum(value(same_day_school_end[(day, school_end_slot)])for school_end_slot in school_end_slots) == 1:
        print("Gemeinsam Schluss am %s" % (days_cleartext[day]))

#############################################
# TODO persönliche präferenzen
